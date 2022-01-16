from models import User,db, Post, PostTag, Tag
from unittest import TestCase
from app import app
from pdb import set_trace
db.drop_all()
db.create_all()

class PostModelTestCase(TestCase):
    """test for posts"""

    def setUp(self):
        Post.query.delete()
        User.query.delete()
        
        # create a test user. We will need the test_user id, as the posts table has a foreign key from users
        test_user = User(first_name = 'Jones', last_name = 'Steven', image_url = 'https://cdn-icons-png.flaticon.com/512/18/18601.png' )
        db.session.add(test_user)
        db.session.commit()
        # need a dynamy user_id as this will change with every iteration
        test_user_id = User.query.filter_by(first_name = 'Jones').one().id
        # Create a test post, set the user_id (for who created the post) as the user_id of test_user
        test_post = Post(title = 'Tea lover', content = 'Secret content', user_id = test_user_id)
        db.session.add(test_post)
        db.session.commit()
        
    
    def tearDown(self):
        
        db.session.rollback()

    
    def test_show_specific_post(self):
        """tests to make sure that the created test_post is being rendered """
        with app.test_client() as client:
            
            post_id = Post.query.filter_by(title = 'Tea lover').one().id
            
            resp = client.get(f'/posts/{post_id}')
            html = resp.get_data(as_text = True)
            
            self.assertIn('Tea lover', html)
            self.assertIn('Secret content', html)

    def test_submit_post_form(self):
        """test to make sure that the submitted post is appearing in the specific
        users page and that the test post is making into the DB"""
        with app.test_client() as client:
            test_user_id = User.query.filter_by(first_name = 'Jones').one().id
            sent = {'title' : 'test title', 'content':'test_content'}

            resp = client.post(f'/users/{test_user_id}/posts/new', data = sent, follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertIn('test title', html)