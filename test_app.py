from models import User,db
from unittest import TestCase
from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db_test'


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for model for User"""

    def setUp(self):
        User.query.delete()

        test_user = User(first_name='Jones', last_name='Steve', image_url = 'https://cdn-icons-png.flaticon.com/512/18/18601.png')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
    
    def test_home_route(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects = True)
            self.assertEqual(resp.status_code,200)
    
    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            self.assertIn('Jones',html)
    
    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertIn('Create New User', html)
            self.assertEqual(resp.status_code,200)
        
    # def test_add_new_user(self):
    #     with app.test_client() as client:
            # sent = {1}

            # resp = client.post('/users/1/delete', follow_redirects = True)
            
            # self.assertNotIn('Jones', html)
            # self.assertEqual(resp.status_code, 200)