import jwt
from datetime import datetime
from app import db, loginm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from hashlib import _hashlib
from time import time
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


@loginm.user_loader
def load_user(id):  # pylint: disable=redefined-builtin
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Borrower', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = _hashlib.openssl_md5(
            self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(  # pylint: disable=redefined-builtin
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except Exception as e:
            print("EXCEPTION FORMAT PRINT:\n{}".format(e))
            return
        return User.query.get(id)


class Borrower(SearchableMixin, db.Model):
    __searchable__ = ['clientname', 'clientemail', 'clientphone',
                      'clientaddress', 'clientcity', 'clientzip', 'clientinfo']
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(64), index=True)
    clientemail = db.Column(db.String(128), index=True, unique=True)
    clientphone = db.Column(db.String(24), index=True)
    clientaddress = db.Column(db.String(100), index=True)
    clientcity = db.Column(db.String(32), index=True)
    clientzip = db.Column(db.String(8), index=True)
    clientinfo = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # def __repr__(self):
    #    return '{}'.format(self.clientname, self.clientss,
    #                       self.clientemail, self.clientphone,
    #                       self.clientaddress, self.clientcity,
    #                       self.clientzip, self.clientinfo)
    def __repr__(self):
        return '<Borrower {}>'.format(self.clientname)
