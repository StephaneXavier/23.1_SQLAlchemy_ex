from flask import Flask,redirect, render_template,session,flash,request
from models import User,connect_db,db
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)
# the db has to be created in advance using terminal, so that we have a link to it
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
# with app.app_context():
#     db.drop_all()
#     db.create_all()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# app.config['SECRET_KEY'] = 'chickenzzz'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()




@app.route('/')
def home_page():
    """redirects to all users list page"""
    return redirect('/users')


@app.route('/users')
def users_list():
    """shows list of current usrs"""
    users = User.query.all()
    return render_template('users_list.html', users=users)


@app.route('/users/new')
def new_user_form():
    """shows form that allows creation of new user"""
    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Handles post request to create new user"""

    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['image_url']

    new_user = User(first_name = first,last_name=last,image_url=image )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')


@app.route('/users/<int:user_id>')
def get_user_info(user_id):
    """Shows page with user information"""
    user = User.query.get_or_404(user_id)
    return render_template('user_page.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """brings user to page that allows editing of user profile"""
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_info(user_id):
    """Handles post request to edit user information"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
  
    db.session.add(user)
    db.session.commit()

    return redirect('/users')



@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """handles delete post of a user"""
    delete_user = User.query.get_or_404(user_id)

    db.session.delete(delete_user)
    db.session.commit()

    return redirect('/users')

