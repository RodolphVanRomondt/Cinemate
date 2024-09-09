
import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
import random
from helper import IMAGE_DEFAULT, add_remove_list

from forms import UserAddForm, LoginForm, EditForm
from models import db, connect_db, User, Movie, List

CURR_USER_KEY = "curr_user"

URL_API = "http://www.omdbapi.com/?apikey=b3726a50&i=tt"
URL_SEARCH = "http://www.omdbapi.com/?apikey=b3726a50"


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('DATABASE_URL', 'postgresql:///capstone_1_db')
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.filter(User.username == session[CURR_USER_KEY]).first()

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If there is already a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                image_url=form.image_url.data,
                password=form.password.data
            )

            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user_signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('user_signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('user_login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out!", "success")
    return redirect("/")

##############################################################################
# General user routes:


@app.route('/user/<username>')
def user_show(username):
    """ Profile for current user. """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.username != username:

        flash("You can't access other user's profile.", "danger")
        return redirect("/")    

    return render_template("user.html")


@app.route('/user/profile', methods=["GET", "POST"])
def profile():
    """ Update profile for current user. """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    username = session[CURR_USER_KEY]

    form = EditForm()

    if form.validate_on_submit():
        user = User.authenticate(username, form.password.data)

        if user:
            try:
                user.username = form.username.data
                user.image_url = form.image_url.data or User.image_url.default.arg

                db.session.commit()

            except IntegrityError:
                flash("Username already taken!", "danger")
                return redirect("/")

            g.user = user
            session[CURR_USER_KEY] = user.username

            flash(f"Profile Updated Successfully!", "success")
            return redirect(f"/user/{ user.username }")

        flash("Invalid credentials. Can't Update The Profile.", 'danger')
        return redirect("/")

    return render_template("/user_edit.html", username=username, form=form)


@app.route('/user/delete', methods=["POST"])
def delete_user():
    """ Delete user. """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    User.query.filter_by(username = g.user.username).delete()

    do_logout()

    db.session.commit()

    flash("User Deleted!", "success")
    return redirect("/")


@app.route("/mylist")
def user_list():
    """ Show the log in user's watchlist. """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    list = [movie.movie_id for movie in g.user.list]

    if not len(list):
        list = None
        return render_template("list.html", list=list)

    movies = []

    for movie_id in list:

        res = requests.get(f"{URL_SEARCH}", params={"i": movie_id}).json()

        if res["Poster"] == "N/A":
            res["Poster"] = IMAGE_DEFAULT

        movies.append(res)

    return render_template("list.html", movies=movies)

@app.route("/movie")
def movie_search():
    """ Show the result page """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if not request.args:
        flash("You must provide a movie title.", "info")
        return redirect("/")

    res = requests.get(f"{URL_SEARCH}", params={"s": request.args["s"]}).json()

    if res["Response"] == "True":

        resM = [movie for movie in res["Search"] if movie["Type"] == "movie"]

        for movie in resM:
            if movie["Poster"] == "N/A":
                movie["Poster"] = IMAGE_DEFAULT

        random.shuffle(resM)
        return render_template("movie_search.html", movies=resM)

    flash(res["Error"].title(), "info")
    return redirect("/")


@app.route("/movie/<imdbID>")
def movie_detail_get(imdbID):
    """ Show a specific movie by its imdbID. """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    m_db = Movie.query.filter(Movie.id == imdbID).first()

    if not m_db:
        movie = Movie(id=imdbID)
        db.session.add(movie)
        db.session.commit()

    movie = requests.get(f"{URL_SEARCH}", params={"i": imdbID}).json()

    if movie["Poster"] == "N/A":
        movie["Poster"] = IMAGE_DEFAULT

    list = [movie.movie_id for movie in g.user.list]

    return render_template("movie.html", movie=movie, list=list)

@app.route("/movie/<imdbID>", methods=["POST"])
def movie_detail_post(imdbID):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    add_remove_list(imdbID, g.user.list)

    return redirect(f"/movie/{imdbID}")

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no search bar
    - show 15 random movies
    """

    movies = Movie.query.all()
    random.shuffle(movies)

    movie_api = []

    for movie in movies[:15]:

        res = requests.get(f"{URL_SEARCH}", params={"i": movie.id}).json()

        if res["Poster"] == "N/A":
            res["Poster"] = IMAGE_DEFAULT

        movie_api.append(res)

    if CURR_USER_KEY not in session:

        return render_template("home-anon.html", movies=movie_api)

    return render_template('home.html', movies=movie_api)


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
