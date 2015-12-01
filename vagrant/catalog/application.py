# !/usr/bin/env python
# Catalog Items Application is Copyright 2015 by Deanna M. Wagner.  This app
# displays a selection of exercises, based on their category.  This file
# application.py contains the functions that display the categories from the
# database, handle the Google OAuth for logging in and out, creating new
# exercises, allow editing and deleting of items that users created, and API
# endpoint display for JSON and XML.
#


from flask import Flask, render_template, request, redirect, session, url_for
from flask import make_response, jsonify, Response
from flask.ext.seasurf import SeaSurf


import psycopg2
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Exercise
import bleach


from oauth2client import client, crypt
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from dict2xml import dict2xml as xmlify


app = Flask(__name__, template_folder='templates')

engine = create_engine('postgresql://fcuser:uhbVCXdr5!Q@localhost:5432/' \
                       'fitcollection')
#engine = create_engine('postgresql://fcuser:mPo75!QsCr89K@localhost:5432/' \
#                       'fitcollection')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@app.route('/')
def main_content():
    """Returns the rendered template for the main page content."""
    categories = db_session.query(Category).all()
    return render_template('main.html', categories=categories)


CLIENT_ID = "462353067619-htn9r5tpot8rt74920q4akn4m03al3km.apps." +\
             "googleusercontent.com"
APPS_DOMAIN_NAME = "http://localhost:5000"
@app.route('/tokensignin/', methods=['POST'])
def token_signin():
    """Returns the response of a user attempting to login with Google."""
    try:
        if not "google_user_id" in session:
            token = request.form['idtoken']
            idinfo = client.verify_id_token(token, CLIENT_ID)
            # If multiple clients access the backend server:
            if idinfo['aud'] != CLIENT_ID:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', \
                                     'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if datetime.fromtimestamp(idinfo['exp']) < datetime.now():
                raise crypt.AppIdentityError("Token is expired.")
            session['google_user_id'] = idinfo['sub']
    except crypt.AppIdentityError:
        # Invalid token
        raise crypt.AppIdentityError("Token is invalid.")
    #TODO this id needs to be stored so we can use it to see if users can
    # edit or delete exercises
    return Response("google_user_id" + session['google_user_id'], \
                    mimetype='application/text')


@app.route('/tokensignout/', methods=['POST'])
def token_signout():
    """Returns the response of a user attempting to logout with Google."""
    if "google_user_id" in session and session["google_user_id"] == \
        request.form['idtoken']:
        session.pop('google_user_id')
    return Response("User signed out", mimetype='application/text')


@app.route('/<string:category_url>/')
def cat_content(category_url):
    """Returns the rendered template based on the category url.

    Args:
      category_url: the url of the exercise category.
    """
    categories = db_session.query(Category).all()
    cat = db_session.query(Category).filter_by(url = "/" + category_url).first()
    cat_items = db_session.query(Exercise).filter_by(category_id = cat.id)
    return render_template('cat_items.html', categories = categories, \
                           category_name = cat.name, \
                           category = cat_items,
                           category_url = cat.url)


#TODO SQL & JS Injection with SQLAlchemy
@app.route('/<string:category_url>/create/', methods=['GET','POST'])
def create_item(category_url):# we need to know which category
    """Returns the rendered template based on the category url.

    The rendered page contains a form to create new items if user is logged in.

    Args:
      category_url: the url of the exercise category.
    """
    categories = db_session.query(Category).all()
    if request.method == 'POST' and 'google_user_id' in session:
        cat = db_session.query(Category).filter_by(url = "/" + category_url). \
            first()
        new_item = Exercise(name = bleach.clean(request.form['name']), \
                    description = bleach.clean(request.form['description']), \
                    image_link = bleach.clean(request.form['image_link']), \
                    category_id = cat.id, \
                    creator_id = session['google_user_id'])
        db_session.add(new_item)
        db_session.commit()
        return redirect("/" + category_url)
    return render_template('create_items.html', \
                           category_url = "/" + category_url, \
                           categories = categories)


@app.route('/<string:category_url>/<int:exercise_id>/edit/', \
           methods=['GET','POST'])
def edit_item(category_url, exercise_id):
    """Returns the rendered template based on the category url.

    The rendered page contains a form to edit items if user is logged in and if
    the user is the one who created the item in the first place.

    Args:
      category_url: the url of the exercise category.
      exercise_id: the id of the exercise item.
    """
    categories = db_session.query(Category).all()
    exercise = db_session.query(Exercise).filter_by(id = exercise_id).one()
    if request.method == 'POST' and 'google_user_id' in session and \
        session['google_user_id'] == exercise.creator_id:
        exercise.name = bleach.clean(request.form['name'])
        exercise.description = bleach.clean(request.form['description'])
        exercise.image_link = bleach.clean(request.form['image_link'])
        db_session.commit()
        return redirect("/" + category_url)#TODO change to category page
    return render_template('edit_items.html', \
                           category_url = "/" + category_url, \
                           categories = categories, \
                           exercise_id = exercise_id, \
                           exercise = exercise)


@app.route('/<string:category_url>/<int:exercise_id>/delete/', methods=['GET', \
                                                                        'POST'])
def delete_item(category_url, exercise_id):
    """Returns the rendered template based on the category url.

    The rendered page contains a form to delete items if user is logged in and
    if the user is the one who created the item in the first place.

    Args:
      category_url: the url of the exercise category.
      exercise_id: the id of the exercise item.
    """
    categories = db_session.query(Category).all()
    exercise = db_session.query(Exercise).filter_by(id = exercise_id).one()
    if request.method == 'POST' and 'google_user_id' in session and \
        session['google_user_id'] == exercise.creator_id:
        cat = db_session.query(Category).filter_by(url = "/" + category_url). \
            first()
        db_session.delete(exercise)
        db_session.commit()
        return redirect("/" + category_url)
    return render_template('delete_items.html', \
                           category_url = "/" + category_url, \
                           categories = categories, \
                           exercise_id = exercise_id, \
                           exercise = exercise)


@app.errorhandler(404)
def page_not_found(e):
    """Returns the rendered template based on e if the page does not exist.

    Args:
      e: the erroneous url fragment that does not exist.
    """
    return render_template("404.html")


@app.route('/api/categories/<int:category_id>/', methods=['GET'])
def category_api(category_id):
    """Returns the response, the API data, based on the category id.

    Checks header for 'ACCEPT' and if json returns, json else if xml return xml
    for a given exercise category.

    Args:
      category_id: the id of the exercise category.
    """
    category = db_session.query(Category).filter_by(id = category_id).one()
    accept = request.headers.get('ACCEPT')
    resp = None
    if accept == "application/json":
        resp = jsonify(category.serialize)
    else:
        xml = xmlify(category.serialize, wrap="category", indent="  ")
        resp = Response(xml, mimetype='application/xml')
    return resp


@app.route('/api/categories/', methods=['GET'])
def categories_api():
    """Returns the response, the API data, of all categories.

    Checks header for 'ACCEPT' and if json returns, json else if xml return xml
    for all exercise categories.
    """
    categories = db_session.query(Category).all()
    accept = request.headers.get('ACCEPT')
    resp = None
    if accept == "application/json":
        resp = "["
        i = 0
        for category in categories:
            resp += jsonify(category.serialize).get_data()
            if i < len(categories) - 1:
                resp += (",")
            i += 1
        resp += ("]")
        resp = Response(resp, mimetype='application/json')
    else:
        resp = "<categories>"
        for category in categories:
            resp += "\n"
            resp += xmlify(category.serialize, wrap="category", indent="  ")
        resp += ("\n</categories>")
        resp = Response(resp, mimetype='application/xml')
    return resp


@app.route('/api/exercises/<int:exercise_id>/', methods=['GET'])
def exercise_api(exercise_id):
    """Returns the response, the API data, based on the exercise id.

    Checks header for 'ACCEPT' and if json returns, json else if xml return xml
    for a given exercise id.

    Args:
      exercise_id: the id of the exercise item.
    """
    exercise = db_session.query(Exercise).filter_by(id = exercise_id).one()
    accept = request.headers.get('ACCEPT')
    resp = None
    if accept == "application/json":
        resp = jsonify(exercise.serialize)
    else:
        xml = xmlify(exercise.serialize, wrap="exercise", indent="  ")
        resp = Response(xml, mimetype='application/xml')
    return resp


@app.route('/api/exercises/', methods=['GET'])
def exercises_api():
    """Returns the response, the API data, of all exercises.

    Checks header for 'ACCEPT' and if json returns, json else if xml return xml
    for all exercise categories.
    """
    exercises = db_session.query(Exercise).all()
    accept = request.headers.get('ACCEPT')
    resp = None
    if accept == "application/json":
        resp = "["
        i = 0
        for exercise in exercises:
            resp += jsonify(exercise.serialize).get_data()
            if i < len(exercises) - 1:
                resp += (",")
            i += 1
        resp += ("]")
        resp = Response(resp, mimetype='application/json')
    else:
        resp = "<exercises>"
        for exercise in exercises:
            resp += "\n"
            resp += xmlify(exercise.serialize, wrap="exercise", indent="  ")
        resp += ("\n</exercises>")
        resp = Response(resp, mimetype='application/xml')
    return resp


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'S6T4o9ramSyTWCa6r!msy9D^uDE'
    csrf = SeaSurf(app)
    app.run(host='0.0.0.0', port=80)
    #app.run(host='0.0.0.0')
