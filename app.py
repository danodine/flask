from flask import Flask, render_template, request, redirect, url_for
import json


def read_file():
    with open('posts.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def write_file(file):
    with open('posts.json', 'w', encoding='utf-8') as new_file:
        json.dump(file, new_file, ensure_ascii=False, indent=4)


def fetch_post_by_id(id):
    data = read_file()
    for post in data:
        if post['id'] == id:
            return post


app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = read_file()
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = read_file()
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        new_id = blog_posts[-1]["id"] + 1
        blog_posts.append({"id": new_id, "author": author, "title": title, "content": content})
        write_file(blog_posts)
        return render_template('index.html', posts=blog_posts)
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = read_file()
    posts = [post for post in blog_posts if post['id'] != post_id]
    write_file(posts)
    blog_posts_new = read_file()
    return render_template('index.html', posts=blog_posts_new)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = read_file()
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        for p in blog_posts:
            if p['id'] == post_id:
                p['title'] = request.form.get('title')
                p['author'] = request.form.get('author')
                p['content'] = request.form.get('content')
                break

        # Update the post in the JSON file
        write_file(blog_posts)
        # Redirect back to index
        return redirect(url_for('index'))
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
