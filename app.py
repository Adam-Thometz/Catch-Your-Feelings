from flask import Flask, render_template, redirect, flash, g, session, request
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
import os
from forms import LoginForm, RegistrationForm
from spotify_auth import get_auth, get_user_token

from models import db, connect_db, User, Recording, Feeling
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = 'curr_user'
ACCESS_TOKEN = 'access_token'

TOKEN = ''

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///catch_your_feelings'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'the-ocean-firmament'

connect_db(app)
debug = DebugToolbarExtension(app)

#################
# Route helpers #
#################

@app.before_request
def add_user_to_g():
  """Function used to add a logged-in user to the global state"""
  if CURR_USER_KEY in session:
    g.user = User.query.get(session[CURR_USER_KEY])
  else:
    g.user = None

def login_required(f):
  @wraps(f)
  def func(*args, **kwargs):
    if g.user:
      return f(*args, **kwargs)
    else:
      flash("Please log in first")
      return redirect('/')
  return func

def do_login(user):
  """Login by adding user to session"""
  session[CURR_USER_KEY] = user.id

################################
# Feeling Catcher + About Page #
################################

@app.route('/')
def feeling_catcher():
  """Feeling Catcher page"""
  return render_template('index.html')

@app.route('/about')
def about_page():
  """About page"""
  return render_template('about.html')

####################
# User Auth routes #
####################

@app.route('/register', methods=["GET", "POST"])
def register():
  """Register new user"""
  form = RegistrationForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data

    new_user = User.register(username, password, email)
    try:
      db.session.add(new_user)
      db.session.commit()
    except IntegrityError:
      flash('There is already a user with that username or email. Try again.', 'danger')
      return redirect('/register')
    
    do_login(new_user)
    flash('Account successfully created!', 'success')
    return redirect('/')
  else:
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
  """Login user"""
  if g.user:
    flash("You're already logged in!")
    return redirect('/')

  form = LoginForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    user = User.login(username, password)
    if user:
      do_login(user)
      flash(f"Welcome back {user.username}", "success")
      return redirect('/')
    else:
      flash("Invalid login", "danger")
  else:
    return render_template('auth/login.html', form=form)

@login_required
@app.route('/logout', methods=["POST"])
def logout():
  """Log a user out"""
  session.pop(CURR_USER_KEY)
  flash('Successfully logged out', 'primary')
  return redirect('/')

#######################
# Spotify Auth Routes #
#######################

@app.route('/auth-spotify')
def start_auth():
  res = get_auth()
  return redirect(res)

@app.route('/callback/')
def auth_spotify():
  get_user_token(request.args['code'])
  return redirect('/')