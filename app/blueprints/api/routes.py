from . import api
from flask import request, jsonify
from app.models import Post, db

# CRUD

# Creating a post
@api.post('/create_post')
def create_post_api():
    data = request.get_json()

    title = data['title']
    caption = data['caption']
    img_url = data['img_url']
    user_id = data["user_id"]

    # Create an instance of the Post Model
    post = Post(title, caption, img_url, user_id)

    # adding to our db
    db.session.add(post)
    db.session.commit()

    # return a jsonfied response to the user
    return jsonify({
        'status': 'ok',
        'message': f'Post "{title}" has been successfully created'
    })

# Viewing all posts
@api.get('/view_all_posts')
def view_all_posts_api():
    posts = Post.query.all()
    all_posts = []
    for post in posts:
        post_dict = {
            'id': post.id,
            'title': post.title,
            'caption': post.caption,
            'img_url': post.img_url,
            'user_id': post.user_id
        }
        all_posts.append(post_dict)
    
    return jsonify({
        'status': 'ok',
        'posts': all_posts
    })

# Viewing a singular post
@api.get('/get_post/<int:post_id>')
def get_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        post_dict = {
            'id': post.id,
            'title': post.title,
            'caption': post.caption,
            'img_url': post.img_url,
            'user_id': post.user_id
        }
        return jsonify({
            'status': "ok",
            'post': post_dict
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Post does not exist!'
        })

# Updating a post
@api.put('/update_post/<int:post_id>')
def update_post_api(post_id):
    post = Post.query.get(post_id)
    data = request.get_json()

    if post:
        post.title = data['title']
        post.caption = data['caption']
        post.img_url = data['img_url']

        # update changes to db
        db.session.commit()

        return jsonify({
            'status': 'ok',
            'message': f'Post "{post.title}" has been updated!'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Post does not exist!'
        })

# Deleting a post
@api.delete('/delete_post/<int:post_id>')
def delete_post_api(post_id):
    post = Post.query.get(post_id)

    if post:
        db.session.delete(post)
        db.session.commit()

        return jsonify({
            'status': 'ok',
            'message': f'Post "{post.title}" has been deleted!'
        })