from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user

news_bp = Blueprint("news", __name__)

@news_bp.route("/")
def index():
    # require login or guest session before showing news
    if not (current_user.is_authenticated or session.get('guest')):
        return redirect(url_for('auth.login'))
    from models import News
    # optional category filtering
    category = request.args.get('category')
    if category:
        news = News.query.filter_by(category=category).order_by(News.created_at.desc()).all()
    else:
        news = News.query.order_by(News.created_at.desc()).all()

    # list of categories for simple filtering UI
    categories = [c[0] for c in News.query.with_entities(News.category).filter(News.category != None).distinct().all()]
    return render_template("index.html", news=news, categories=categories, selected_category=category)

@news_bp.route("/news/<int:id>", methods=["GET", "POST"])
def news_detail(id):
    from models import News, Comment
    from extensions import db

    news = News.query.get_or_404(id)
    # top-level comments only; replies are accessed via comment.replies
    comments = Comment.query.filter_by(news_id=id, parent_id=None).order_by(Comment.created_at.asc()).all()

    if request.method == "POST" and current_user.is_authenticated:
        parent_id = request.form.get('parent_id')
        comment = Comment(
            content=request.form["content"],
            user_id=current_user.id,
            news_id=id,
            parent_id=int(parent_id) if parent_id else None
        )
        db.session.add(comment)
        db.session.commit()
        # redirect to avoid form resubmission
        return redirect(url_for('news.news_detail', id=id))

    return render_template("news_detail.html", news=news, comments=comments)

@news_bp.route('/bookmark/<int:id>')
def toggle_bookmark(id):
    from extensions import db
    from models import Bookmark, News

    if not current_user.is_authenticated:
        # redirect to login; guests cannot bookmark
        return redirect(url_for('auth.login'))

    news = News.query.get_or_404(id)
    bm = Bookmark.query.filter_by(user_id=current_user.id, news_id=id).first()
    if bm:
        db.session.delete(bm)
        db.session.commit()
    else:
        bm = Bookmark(user_id=current_user.id, news_id=id)
        db.session.add(bm)
        db.session.commit()

    return redirect(url_for('news.news_detail', id=id))
