# Client ID for web application
# Client ID	325598442678-t9j4mh1u8vvbjhmah628176n884k7c9r.apps.googleusercontent.com
# Email address	325598442678-t9j4mh1u8vvbjhmah628176n884k7c9r@developer.gserviceaccount.com
# Client secret	O_ehB06bO7QNjTD7Accw1LWh
# Redirect URIs	none
# JavaScript origins	http://localhost:8000

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items, Categories, Subcategories, Users
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "item-catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def list_categories():
	returnString = '<ul>'
	categories = session.query(Categories).all()
	for c in categories:
		returnString = returnString + '<li data-jstree=\'{"opened":false,"selected":false,"url":"#"}\'>' + c.name + '<ul>'
		subcategories = session.query(Subcategories).filter_by(category_id = c.id)
		for s in subcategories:
			returnString = returnString + '<li data-jstree=\'{"url":"' + str(c.id) + '/' + str(s.id) + '"}\'>' + s.name + '</li>'
		
		returnString = returnString + '</ul>'
	returnString = returnString + '</li></ul>'
	return returnString

def createUser(login_session):
	newUser = Users(name=login_session['username'], email=login_session[
				   'email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(Users).filter_by(email=login_session['email']).one()
	return user.id


def getUserInfo(user_id):
	user = session.query(Users).filter_by(id=user_id).one()
	return user


def getUserID(email):
	try:
		user = session.query(Users).filter_by(email=email).one()
		return user.id
	except:
		return None
	
@app.route('/')
def showItems():
	categories_list = list_categories()
	return render_template('items.html', categories_list = categories_list, user = login_session.get('username'), access_token = login_session.get('access_token'))
	
@app.route('/subcategory_items/<int:category_id>/<int:subcategory_id>')
def getItemsBySub(category_id, subcategory_id):
	items = session.query(Items).filter_by(subcategory_id=subcategory_id)
	return render_template('items_by_sub.html', items = items, access_token = login_session.get('access_token'), category_id=category_id, subcategory_id=subcategory_id)
	
@app.route('/latest_items')
def getLatestItems():
	items = session.query(Items).order_by(Items.added.desc()).limit(5)
	return render_template('latest_items.html', items = items, access_token = login_session.get('access_token'))

@app.route('/item_info/<int:item_id>', methods=['GET', 'POST'])
def showItemInfo(item_id):
	item = session.query(Items).filter_by(id=item_id).one()
	if request.method == 'POST':
		item.title = request.form['title']
		item.description = request.form['description']
		session.commit()
		return redirect(url_for('getItemsBySub', category_id = item.category_id, subcategory_id = item.subcategory_id))
	else:
		return render_template('item_info.html', item = item, access_token = login_session.get('access_token'))

@app.route('/item/delete/<int:item_id>', methods=['GET', 'POST'])
def deleteItem(item_id):
	item = session.query(Items).filter_by(id=item_id).one()
	if request.method == 'POST':
		category_id = item.category_id
		subcategory_id = item.subcategory_id
		session.delete(item)
		session.commit()
		return redirect(url_for('getItemsBySub', category_id = item.category_id, subcategory_id = item.subcategory_id))
	else:
		return render_template('item_delete.html', item = item, access_token = login_session.get('access_token'))

@app.route('/item/new/<int:category_id>/<int:subcategory_id>', methods=['GET', 'POST'])
def newItem(category_id, subcategory_id):
	if request.method == 'POST':
		newItem = Items(title=request.form['title'], description=request.form['description'], category_id=request.form['category_id'], subcategory_id=request.form['subcategory_id'])
		session.add(newItem)
		flash('New item %s Successfully Created' % newItem.title)
		session.commit()
		return redirect(url_for('getItemsBySub', category_id = newItem.category_id, subcategory_id = newItem.subcategory_id))
	else:
		category = session.query(Categories).filter_by(id=category_id).one()
		subcategory = session.query(Subcategories).filter_by(id=subcategory_id).one()
		return render_template('new_item.html', access_token = login_session.get('access_token'), category=category, subcategory=subcategory)
		
@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)
	
@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
		# return credentials.access_token
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

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
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()
	
	login_session['access_token'] = access_token
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	login_session['provider'] = 'google'

	# see if user exists, if it doesn't make a new one
	user_id = getUserID(data["email"])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output

@app.route('/logout')
def logout():
	# only if signed in with Google Plus
	if not login_session.get('gplus_id') is None:
		gdisconnect()
	return redirect('/')

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

	if result['status'] == '200':
		# Reset the user's sesson.
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['access_token']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		# invalid token
		response = make_response(
			json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)