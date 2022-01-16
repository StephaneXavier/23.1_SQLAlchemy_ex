from models import User,Post,Tag,PostTag, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name = 'George', last_name = 'Daher', image_url = 'https://cdn-icons-png.flaticon.com/512/18/18601.png')
u2 = User(first_name = 'Stephane', last_name = 'Comeau',image_url = 'https://cdn-icons-png.flaticon.com/512/18/18601.png')
u3 = User(first_name = 'Steve', last_name = 'Jones',image_url = 'https://cdn-icons-png.flaticon.com/512/18/18601.png')
u4 = User(first_name = 'Sean', last_name = 'Mckenna')

db.session.add_all([u1,u2,u3,u4])

p1 = Post(title = 'George rules', content = 'Habibi time!', user_id = 1)
p2 = Post(title = 'Stephane programs', content = 'studying hacker stuff', user_id = 2)
p3 = Post(title = 'Staff sgt', content = 'doing stuff', user_id = 3)
p4 = Post(title = 'Pre-rcmp', content = 'I used to be a lumberjack', user_id = 4)
p5 = Post(title = 'George is curious', content = 'Not the banana kind', user_id = 1)

db.session.add_all([p1,p2,p3,p4,p5])

t1 = Tag(name ='Like')
t2 = Tag(name = 'Dislike')
t3 = Tag(name = 'Bookmark')

db.session.add_all([t1,t2,t3])
db.session.commit()

pt1 = PostTag(post_id=1,tag_id=1)
pt2 = PostTag(post_id=2,tag_id=3)
pt3 = PostTag(post_id=3,tag_id=2)
pt4 = PostTag(post_id=4, tag_id = 1)
pt5 = PostTag(post_id=5, tag_id = 2)
pt6 = PostTag(post_id=1, tag_id=3)

db.session.add_all([pt1,pt2,pt3,pt4,pt5,pt6])

db.session.commit()