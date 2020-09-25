import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__, template_folder="templates")


def load_posts():
    posts = []
    for file in os.listdir("posts"):
        if file.endswith(".txt"):
            with open("posts" + os.path.sep + file) as rf:
                post = {}
                doc = ""
                post["title"] = rf.readline().rstrip("\n")
                post["author"] = rf.readline().rstrip("\n")
                post["date"] = rf.readline().rstrip("\n")
                post["content"] = []
                paragraph = ""
                for line in rf:
                    if line == "\n":
                        post["content"].append(paragraph)
                        paragraph = ""
                    else:
                        paragraph += line.rstrip("\n")
                    doc += line.rstrip("\n") + " "
                post["content"].append(paragraph)
                post["readtime"] = round(len(doc.split()) / 275)
                posts.append(post)
    return posts


posts = load_posts()


@app.route("/")
def home():
    return render_template("home.html", posts = posts)


@app.route("/<date>/<title>")
def post(date, title):
    for post in posts:
        if post["title"] == title and post["date"] == date:
            return render_template("post.html", post = post)

if __name__ == "__main__":
    app.run()