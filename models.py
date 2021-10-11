from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
  """Connect to database"""
  db.app = app
  db.init_app(app)

class User(db.Model):
  """User model"""

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.Text, nullable=False, unique=True)
  password = db.Column(db.Text, nullable=False)
  email = db.Column(db.Text, nullable=False)
  
  library = db.relationship('Recording', secondary="libraries", backref="users")
  feelings = db.relationship('Feeling')

  # Registration method
  @classmethod
  def register(cls, username, password, email):
    """Register user with a hashed password"""
    hashed_pw = bcrypt.generate_password_hash(password)
    hashed_utf8 = hashed_pw.decode('utf8')

    return cls(username=username, password=hashed_utf8, email=email)
  
  # Login method
  @classmethod
  def login(cls, username, password):
    """Authenticate a user for logging in"""
    user = cls.query.filter_by(username=username).first()

    if user:
      is_auth = bcrypt.check_password_hash(user.password, password)
      if is_auth:
        return user

    return False

class Recording(db.Model):
  """Recording model"""

  __tablename__ = "recordings"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.Text)
  artist = db.Column(db.Text)
  spotify_uri = db.Column(db.Text)
  valence = db.Column(db.Float)
  energy = db.Column(db.Float)

class Feeling(db.Model):
  """Feeling model"""

  __tablename__ = "feelings"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  valence = db.Column(db.Text)
  energy = db.Column(db.Text)
  time = db.Column()
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Library(db.Model):
  """User-Recording relationship"""

  __tablename__ = "libraries"

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'), primary_key=True)