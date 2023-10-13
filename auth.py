from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
import db


def register(username, password):
    db = get_db()
    error = None

    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {username} is already registered."

    return error


def login(username, password):
    d = get_db()
    error = None
    user = d.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        db.session = {}
        db.session['user_id'] = user['id']

    return error


def load_logged_in_user():
    user_id = db.session.get('user_id')

    if user_id is None:
        db.USER = None
    else:
        db.USER = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def logout():
    db.session = {}
    db.USER = None
    return '/login'


def login_required():
    if db.USER is None:
        return '/login'
    return None
