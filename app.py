# ******************************************************************************************
# ******************************************************************************************
# the tables are not automatically created. Either create them manually or run the seed file.
# ******************************************************************************************
# ******************************************************************************************
from flask import Flask,redirect, render_template,session,flash,request
from models import User,connect_db,db, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'chickenzzz'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()


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
    """Grabs information from the new user form, adds it to the SQL DB with a new instance of User class"""

    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['image_url']

    new_user = User(first_name = first,last_name=last,image_url=image )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')



@app.route('/users/<int:user_id>')
def get_user_info(user_id):
    """Shows page with user information, including all of the users' posts"""
    user = User.query.get_or_404(user_id)
    
    posts = Post.query.filter_by(user_id = user_id).all()
    return render_template('user_page.html', user=user, posts = posts)



@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """brings user to page that allows editing of user profile"""
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user = user)



@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_info(user_id):
    """Handles edited user information. If there is new information, that instance of user.key is set to 
    new info"""
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



@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Render the page to add new post. Get all the tags that have currently been
    created and display them as checkboxes that can be applied to the newly created post"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('post_form.html', user_id=user_id, user = user, tags = tags)



@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_post_form(user_id):
    """ Handles the submission of a new post. Garb all the information that the user created (title, content,
    and the checkboxes checked). Create a new instance of Post. Create new instance(s) in the
    PostTag based on what tags have been selected to be with the post"""
    title = request.form['title']
    content = request.form['content']
    tags_id = request.form.getlist('tag')
    
    post = Post(title = title, content = content, user_id = user_id)
    
    db.session.add(post)
    db.session.commit()
    
    for tag_id in tags_id: 
        db.session.add(PostTag(post_id = post.id, tag_id = tag_id ))

    db.session.commit()

    flash('Post added!')
    return redirect (f'/users/{user_id}')



@app.route('/posts/<int:post_id>')
def show_specific_post(post_id):
    """Show the selected post along with it's associated tags"""
    post = Post.query.get(post_id)
    tags = post.tags

    return render_template('specific_post.html', post_id = post_id, post = post, tags=tags)



@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show the edit for for the specific post. """
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    
    return render_template('post_edit.html',post = post, tags = tags)



@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def submit_post_edit_form(post_id):
    """Handle the post request to modify the selected post. If the content is not empty, set respectively
    the title and/or content to the new content. Delete all previous associations in the posts_tags table,
    then re-update by adding the new data in posts_tags table that reflects what tags the user has selected
    or unselected during the editing"""
    PostTag.query.filter_by(post_id=post_id).delete()
    db.session.commit()

    title = request.form['title']
    content = request.form['content']
    post = Post.query.get(post_id)
    tags_id = request.form.getlist('tag')

    if title != '':
        post.title = title 
    if content != '':
        post.content = content
    
    
    for tag_id in tags_id:
        pt =PostTag(post_id=post_id,tag_id = tag_id)
        db.session.add(pt)
        
    db.session.add(post)
    db.session.commit()

    flash('Post edited!')
    return redirect(f'/users/{post.user_id}')



@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Handle post request to delete selected post."""
    post = Post.query.get_or_404(post_id)
    PostTag.query.filter_by(post_id=post_id).delete()
    
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted!')

    return redirect(f'/users/{post.user_id}')


@app.route('/tags')
def show_tags():
    """Show all currently created tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)


@app.route('/tags/<int:tag_id>')
def show_specific_tag(tag_id):
    """Show all posts currently associated to the selected tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    
    return render_template('tag_info.html', tag = tag, posts = posts)

@app.route('/tags/new')
def render_tag_form():
    """Renders the form to create a new tag"""
    return render_template('new_tag_form.html')

@app.route('/tags/new', methods = ['POST'])
def submit_new_tag():
    """Handle post request for the creation of new tag. Grab the information from the form then 
    create a new instance of the Tag class which is then sent to the SQL DB."""
    tag_name = request.form['tag_name']
    new_tag = Tag(name = tag_name)
    db.session.add(new_tag)
    db.session.commit()

    flash('New tag added!')

    return redirect('/tags')



@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Render form that allows user to edit selected tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag = tag)



@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def submit_edit_tag(tag_id):
    """Handle post request that modifies selected tag."""
    edited_tag_name = request.form['tag_name']
    tag = Tag.query.get_or_404(tag_id)
    tag.name = edited_tag_name
    
    db.session.add(tag)
    db.session.commit()
    
    flash('Tag edited!')
    return redirect('/tags')



@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    """Handle post request that deletes the selected tag."""
    tag = Tag.query.filter(Tag.id == tag_id)
    posts_tags_delete = PostTag.query.filter(PostTag.tag_id == tag_id)

    posts_tags_delete.delete()
    tag.delete()
    db.session.commit()

    return redirect('/tags')