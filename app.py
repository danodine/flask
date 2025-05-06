from flask import Flask, render_template, request
import json

with open('posts.json', 'r', encoding='utf-8') as file:
    blog_posts = json.load(file)

print(blog_posts)



app = Flask(__name__)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(debug=True)
