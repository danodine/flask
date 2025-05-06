from flask import Flask, render_template, request
import json

def read_file():
    with open('posts.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def write_file(file):
    with open('posts.json', 'w', encoding='utf-8') as new_file:
        json.dump(file, new_file, ensure_ascii=False, indent=4)

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


if __name__ == '__main__':
    app.run(debug=True)
