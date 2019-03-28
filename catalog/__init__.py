# Required Modules are imported to this python file
from flask import Flask, render_template, \
    url_for, request, redirect,\
    flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from db_create import Branch, Course, User, Base
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import random
import string
import datetime
import json
import httplib2
import requests

# checking user for perform action

from checker import login_required

# Flask instance

app = Flask(__name__)


# GConnect CLIENT_ID

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to database
#engine = create_engine('sqlite:///branchcourse.db',
#                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
engine = create_engine('postgresql://catalog:catalog@localhost/catalog',
                       connect_args={'check_same_thread': False}, echo=True)
# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Login - Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    Gathers data from Google Sign In API and places
    it inside a session variable.
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is'
                                            'already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    try:
        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']
    except psycopg2.OperationalError as e:
        login_session['username'] = "Google User"
        login_session['picture'] = "http://tiny.cc/lz6m2y"
        login_session['email'] = "Google Email"

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = '<html><body bgcolor="#E6E6FA">'
    output += '<h1>Hello, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'+login_session['picture']+'"'
    output += ' style = "width: 300px; height: 300px;border-radius: 150px;'
    output += ' webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    output += '</body></html>'
    flash("You are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    try:
        result['status'] == '200'
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = redirect(url_for('showCatalog'))
        flash("You are now logged out.")
        return response
    except Exception as e:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'+e, 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Show Home page


@app.route('/')
@app.route('/courses/')
def showCatalog():
    branches = session.query(Branch).order_by(asc(Branch.name))
    courses = session.query(Course).order_by(desc(Course.date))
    if 'username' not in login_session:
        return render_template('public_Catalog.html',
                               branches=branches,
                               courses=courses)
    else:
        return render_template('Catalog.html', branches=branches,
                               courses=courses)

# Add a new Branch to database


@app.route('/catalog/newbranch', methods=['GET', 'POST'])
@login_required
def newBranch():
    if request.method == 'POST':
        newbranch = Branch(name=request.form['name'],
                           user_id=login_session['user_id'])
        session.add(newbranch)
        session.commit()
        flash(newbranch.name+" branch Created")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newBranch.html')

# Edit a branch from database


@app.route('/catalog/<branch_name>/edit', methods=['GET', 'POST'])
@login_required
def editBranch(branch_name):
    branchToEdit = session.query(Branch).filter_by(name=branch_name).one()

    # Prevent logged-in user to edit other user's branch

    if branchToEdit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert(' You are not authorized"\
                "to edit this branch."\
                "Please create your own " \
               "branch " \
               "in order to edit.');}</script><body onload='myFunction()'>"
    # Save edited branch to the database

    if request.method == 'POST':
        branchToEdit.name = request.form['name']
        session.add(branchToEdit)
        session.commit()
        flash(branchToEdit.name+" branch Edited")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editBranch.html', branch=branchToEdit)

# Delete a branch from database


@app.route('/catalog/<branch_name>/delete/', methods=['GET', 'POST'])
@login_required
def deleteBranch(branch_name):
    branchToDelete = session.query(Branch).filter_by(name=branch_name).one()

    # Prevent logged-in user to delete other user's branch

    if branchToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
            "to delete this branch. Please create your own " \
               "branch " \
               "in order to delete.');}</script><body onload='myFunction()'>"

    # Delete branch from the database

    if request.method == 'POST':
        session.delete(branchToDelete)
        session.commit()
        flash(branchToDelete.name+" Branch Deleted Successfully")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletebranch.html', branch=branchToDelete)


# Show all courses in a branch from database

@app.route('/catalog/<branch_name>/courses')
def showBranchCourses(branch_name):
    branches = session.query(Branch).order_by(asc(Branch.name))
    chosenBranch = session.query(Branch).filter_by(name=branch_name).one()
    courses = session.query(Course).filter_by(
        branch_id=chosenBranch.id).order_by(asc(Course.name))
    creator = getUserInfo(chosenBranch.user_id)
    if 'username' not in login_session or\
       creator.id != login_session['user_id']:
        return render_template('publicBranchCourses.html',
                               branches=branches,
                               chosenBranch=chosenBranch,
                               courses=courses)
    else:
        return render_template('showBranchCourses.html',
                               branches=branches,
                               chosenBranch=chosenBranch,
                               courses=courses)

# Show information of a specific course


@app.route('/catalog/<branch_name>/<course_name>')
def showCourse(branch_name, course_name):
    branch = session.query(Branch).filter_by(
        name=branch_name).one()
    course = session.query(Course).filter_by(
        name=course_name, branch=branch).one()
    creator = getUserInfo(course.user_id)
    if 'username' not in login_session or\
       creator.id != login_session['user_id']:
        return render_template('publicCourse.html', course=course)
    else:
        return render_template('showCourse.html', course=course)

# Add a new course to database


@app.route('/catalog/newcourse', methods=['GET', 'POST'])
@login_required
def newCourse():
    branches = session.query(Branch).order_by(asc(Branch.name))
    if request.method == 'POST':
        addingCourse = Course(
            name=request.form['name'],
            level=request.form['level'],
            price=request.form['price'],
            date=request.form['date'],
            description=request.form['description'],
            image=request.form['image'],
            branch=session.query(
                Branch).filter_by(name=request.form['branch']).one(),
            user_id=login_session['user_id'])
        session.add(addingCourse)
        session.commit()
        flash(addingCourse.name+" Course created Successfully")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCourse.html',
                               branches=branches)

# Edit a course


@app.route('/catalog/<branch_name>/<course_name>/edit',
           methods=['GET', 'POST'])
@login_required
def editCourse(branch_name, course_name):
    branches = session.query(Branch).order_by(asc(Branch.name))
    editingCourseBranch = session.query(Branch).filter_by(
                                        name=branch_name).one()
    editingCourse = session.query(Course).filter_by(
        name=course_name, branch=editingCourseBranch).one()

    # Prevent logged-in user to edit course which belongs to other user

    if editingCourse.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
                "to edit this course. Please create your own course " \
               "in order to edit.');}</script><body onload='myFunction()'>"

    # Save edited course to the database

    if request.method == 'POST':
        if request.form['name']:
            editingCourse.name = request.form['name']
        if request.form['description']:
            editingCourse.description = request.form['description']
        if request.form['date']:
            editingCourse.date = request.form['date']
        if request.form['level']:
            editingCourse.level = request.form['level']
        if request.form['price']:
            editingCourse.price = request.form['price']
        if request.form['branch']:
            editingCourse.branch = session.query(Branch).filter_by(
                name=request.form['branch']).one()
        session.add(editingCourse)
        session.commit()
        flash(editingCourse.name+" Course Edited Successfully")
        return redirect(url_for('showCourse',
                                branch_name=editingCourseBranch.name,
                                course_name=editingCourse.name))
    else:
        return render_template('editCourse.html', branches=branches,
                               editingCourseBranch=editingCourseBranch,
                               course=editingCourse)

# Delete a course from database


@app.route('/catalog/<branch_name>/<course_name>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteCourse(branch_name, course_name):
    branch = session.query(Branch).filter_by(name=branch_name).one()
    deletingCourse = session.query(Course).filter_by(
        name=course_name, branch=branch).one()

    # Prevent logged-in user to delete course which belongs to other user

    if deletingCourse.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
                "to delete this course. Please create your own course " \
               "in order to delete.');}</script><body onload='myFunction()'>"
    # Delete course from the database

    if request.method == 'POST':
        session.delete(deletingCourse)
        session.commit()
        flash(deletingCourse.name+" Course Deleted Successfully")
        return redirect(url_for('showCatalog', branch_name=branch.name))
    else:
        return render_template('deleteCourse.html', course=deletingCourse)

# ------> Get all Courses JSON Data from db


@app.route('/courses/JSON')
def catalogJSON():
    courses = session.query(Course).all()
    return jsonify(Courses=[course.serialize for course in courses])

# -------> Get all courses JSON data in particular branch from db


@app.route('/branches/<int:branch_id>/JSON')
def coursesJSON(branch_id):
    courses = session.query(Course).filter_by(
        branch_id=branch_id).all()
    return jsonify(courses=[course.serialize for course in courses])

# -------> Get all Branches in the format of JSON from db


@app.route('/branches/JSON')
def branchJSON():
    branches = session.query(Branch).all()
    return jsonify(Branches=[branch.serialize for branch in branches])

# --------> Get single partucular Course JSON data from db


@app.route('/branches/course/<int:branch_id>/<int:course_id>/JSON')
def singleCourseJSON(branch_id, course_id):
    course = session.query(Course).filter_by(id=course_id,
                                             branch_id=branch_id).one()
    return jsonify(course=[course.serialize])


if __name__ == '__main__':
    app.secret_key = 'APP_SECRET_KEY'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
