from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    from models import User
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            session.pop('guest', None)
            return redirect(url_for("news.index"))
    return render_template("login.html")

@auth_bp.route("/guest")
def guest():
    # set a simple guest flag in the session (no DB user)
    session['guest'] = True
    return redirect(url_for('news.index'))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    from models import User
    from extensions import db
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
            role='uye'
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    session.pop('guest', None)
    return redirect(url_for("news.index"))

from flask_login import login_required, current_user

@auth_bp.route('/profile')
@login_required
def profile():
    # show current user's profile and their comments
    from models import Comment
    comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).all()
    return render_template('profile.html', user=current_user, user_comments=comments)

@auth_bp.route('/profile/<int:user_id>')
def user_profile(user_id):
    # public view of another user's profile and comments
    from models import User, Comment
    user = User.query.get_or_404(user_id)
    comments = Comment.query.filter_by(user_id=user.id).order_by(Comment.created_at.desc()).all()
    return render_template('profile.html', user=user, user_comments=comments)
