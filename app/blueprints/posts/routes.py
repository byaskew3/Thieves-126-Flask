from . import posts
from .forms import PostForm
from flask import request, redirect, url_for, render_template, flash
from app.models import db, Post
from flask_login import current_user

@posts.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our post form data
        title = form.title.data 
        caption = form.caption.data
        img_url = form.img_url.data
        user_id = current_user.id
        
        # Creating an instance of the Post Model
        new_post = Post(title, caption, img_url, user_id)

        # Adding new post to our database
        db.session.add(new_post)
        db.session.commit()

        flash(f'Successfully created post {title}!', 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('create_post.html', form=form)

@posts.route('/feed')
def feed():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)