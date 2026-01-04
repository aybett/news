from flask import Flask
from flask_login import LoginManager
from extensions import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# uploads config
import os
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# broaden allowed extensions to include office docs and common archives
app.config['ALLOWED_EXTENSIONS'] = {
    'png','jpg','jpeg','gif','bmp','webp','pdf',
    'doc','docx','xls','xlsx','ppt','pptx','txt',
    'zip','rar'
} 

# initialize the shared DB instance with the app
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Add Flask-Migrate for DB migrations (optional)
try:
    from flask_migrate import Migrate
    migrate = Migrate()
except Exception:
    migrate = None

# helper to ensure added columns exist for development SQLite DB
from sqlalchemy import inspect, text

def ensure_db_columns():
    inspector = inspect(db.engine)
    # ensure news.category exists
    if 'news' in inspector.get_table_names():
        cols = [c['name'] for c in inspector.get_columns('news')]
        if 'category' not in cols:
            try:
                with db.engine.begin() as conn:
                    conn.execute(text("ALTER TABLE news ADD COLUMN category TEXT"))
                print('Added missing column: news.category')
            except Exception as e:
                print('Could not add news.category:', e)
    # ensure comment.parent_id exists (table name likely 'comment')
    if 'comment' in inspector.get_table_names():
        cols = [c['name'] for c in inspector.get_columns('comment')]
        if 'parent_id' not in cols:
            try:
                with db.engine.begin() as conn:
                    conn.execute(text("ALTER TABLE comment ADD COLUMN parent_id INTEGER"))
                print('Added missing column: comment.parent_id')
            except Exception as e:
                print('Could not add comment.parent_id:', e)

# Avoid top-level import of User (prevents circular import with models)
from auth import auth_bp
from news import news_bp
from admin import admin_bp

@login_manager.user_loader
def load_user(user_id):
    from models import User
    # use session.get to avoid SQLAlchemy Query.get legacy warning
    return db.session.get(User, int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(news_bp)
app.register_blueprint(admin_bp)

# expose whether a watermark image exists so templates can choose image vs text
@app.context_processor
def inject_watermark():
    uploads_dir = os.path.join(app.static_folder or '', 'uploads')
    watermark_file = None
    # prefer explicit watermark.png
    candidate = os.path.join(uploads_dir, 'watermark.png')
    if os.path.exists(candidate):
        watermark_file = 'watermark.png'
    else:
        # search for any file containing 'chatgpt' (case-insensitive) and use it
        if os.path.isdir(uploads_dir):
            for fname in os.listdir(uploads_dir):
                if 'chatgpt' in fname.lower():
                    watermark_file = fname
                    break
    return {'watermark_file': watermark_file}

if __name__ == "__main__":
    with app.app_context():
        # ensure models are imported so their tables are registered with SQLAlchemy
        import models
        # initialize migrate with app and db so CLI commands work (if available)
        if migrate:
            migrate.init_app(app, db)
        # create tables for quick dev setup if not using migrations yet
        db.create_all()
        # attempt to add missing columns (development convenience only)
        try:
            ensure_db_columns()
        except Exception as e:
            print('Error while ensuring DB columns:', e)
    app.run(debug=True)
