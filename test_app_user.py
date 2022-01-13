from models import User,db, Post
from unittest import TestCase
from app import app
from pdb import set_trace


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db_test'


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for model for User"""

    def setUp(self):
        """Delete all previously created users in the DB. Create a new User instance.
        add said instance to the SQL DB"""
        User.query.delete()

        test_user = User(first_name='Jones', last_name='Steve', image_url = 'https://cdn-icons-png.flaticon.com/512/18/18601.png')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        """Ensure that any pending Flask to SQL object has been wiped from work queue"""
        User.query.delete()
        db.session.rollback()
    
    def test_home_route(self):
        """Ensures that the home route is redirected to /users"""
        with app.test_client() as client:
            resp = client.get('/', follow_redirects = True)
            self.assertEqual(resp.status_code,200)
    
    def test_users_list(self):
        """Ensures that the main page with the user list is properly rendered"""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            self.assertIn('Jones',html)
    
    def test_new_user_form(self):
        """Ensure the new user form page is properly rendered"""
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertIn('Create New User', html)
            self.assertEqual(resp.status_code,200)
        
    def test_add_new_user(self):
        """Tests that route creates a new user then adds it to the /users page. Ensures
        that the SQL DB is also updated"""
        with app.test_client() as client:
            #data to be sent over client as a POST request
            sent = {'first_name':'Tezy', 'last_name' : 'Kaliv', 'image_url' : ''}
            # send a post request to the /users/new POST route. Follow the redirect to /users
            resp = client.post('/users/new', data = sent, follow_redirects = True)
            # get the information from SQL for the newly created user
            new_test_user = User.query.filter_by(first_name = 'Tezy').all()
            # ensure that that 'Tezy' is being displayer on the users page
            self.assertIn('Tezy', resp.get_data(as_text = True))
            self.assertIn('Jones', resp.get_data(as_text = True))
            # ensure that information in 'sent' is in the SQL DB
            self.assertEqual(new_test_user[0].first_name, 'Tezy')
            self.assertEqual(resp.status_code, 200)
    
    def test_delete_user(self):
        """Ensure that you can delete the a user"""
        with app.test_client() as client: 
            # use var jones to get the id of the user
            jones = User.query.filter_by(first_name = 'Jones').all()
            resp = client.post(f'/users/{jones[0].id}/delete', follow_redirects =True)
            # get list of all the users, or if there is none set users to None (thanks to one_or_none() )
            users = User.query.filter_by(first_name = 'Jones').one_or_none()
            # make sure that the user inputed during setUp has been deleted from SQL DB
            self.assertEqual(users,None)
            # grab the users page and make sure that setUp create user is not there anymore.
            resp2 = client.get('/users')
            html = resp2.get_data(as_text =True)
            self.assertNotIn('Jones', resp.get_data(as_text =True))
           
           


