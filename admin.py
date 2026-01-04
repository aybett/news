from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import current_user
import os
import uuid
from werkzeug.utils import secure_filename

def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'pdf'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required():
    # 'editor' role is used for content management
    return current_user.is_authenticated and getattr(current_user, 'role', None) == "editor"

@admin_bp.route("/")
def dashboard():
    if not admin_required():
        return redirect(url_for("news.index"))
    from models import News
    news = News.query.all()
    return render_template("admin/dashboard.html", news=news)

@admin_bp.route("/add", methods=["GET", "POST"])
def add_news():
    if not admin_required():
        return redirect(url_for("news.index"))

    from models import News
    from extensions import db

    if request.method == "POST":
        # create news
        news = News(
            title=request.form["title"],
            content=request.form["content"],
            category=request.form.get('category'),
            author_id=current_user.id
        )

        # handle image upload with error handling
        file = request.files.get('image')
        if file and file.filename and allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_" + secure_filename(file.filename)
            dest = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(dest)
                news.image = filename
                from flask import flash
                flash('Dosya yüklendi: ' + filename)
            except Exception as e:
                from flask import flash
                flash('Dosya kaydedilemedi: ' + str(e))

        db.session.add(news)
        db.session.commit()
        from flask import flash
        flash('Haber eklendi')
        # redirect to the news detail so user sees it immediately
        return redirect(url_for('news.news_detail', id=news.id))


    return render_template("admin/add_news.html")

@admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_news(id):
    if not admin_required():
        return redirect(url_for('news.index'))
    from models import News
    from extensions import db
    n = News.query.get_or_404(id)
    if request.method == 'POST':
        n.title = request.form['title']
        n.content = request.form['content']
        n.category = request.form.get('category')

        # handle new image upload and remove old file
        file = request.files.get('image')
        if file and file.filename and allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_" + secure_filename(file.filename)
            dest = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(dest)
                # delete old file after new file saved
                if n.image:
                    try:
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], n.image))
                    except OSError:
                        pass
                n.image = filename
                from flask import flash
                flash('Dosya yüklendi: ' + filename)
            except Exception as e:
                from flask import flash
                flash('Dosya kaydedilemedi: ' + str(e))

        db.session.commit()
        from flask import flash
        flash('Haber güncellendi')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_news.html', news=n)

@admin_bp.route('/delete/<int:id>')
def delete_news(id):
    if not admin_required():
        return redirect(url_for('news.index'))
    from models import News
    from extensions import db
    n = News.query.get_or_404(id)
    # delete image file if exists
    if n.image:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], n.image))
        except OSError:
            pass
    db.session.delete(n)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/comment/delete/<int:id>')
def delete_comment(id):
    if not admin_required():
        return redirect(url_for('news.index'))
    from models import Comment
    from extensions import db
    c = Comment.query.get_or_404(id)
    news_id = c.news_id
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('news.news_detail', id=news_id))

@admin_bp.route('/users')
def users():
    if not admin_required():
        return redirect(url_for('news.index'))
    from models import User
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/delete/<int:id>')
def delete_user(id):
    if not admin_required():
        return redirect(url_for('news.index'))
    from models import User
    from extensions import db
    u = User.query.get_or_404(id)
    if u.id == current_user.id:
        return redirect(url_for('admin.users'))
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('admin.users'))
