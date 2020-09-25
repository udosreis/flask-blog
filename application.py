import os
from datetime import datetime
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
                post["date"] = datetime.strptime(rf.readline().rstrip("\n"), "%Y-%m-%d")
                post["content"] = []
                
                paragraph = {"text": "", "type": 0}
                for line in rf:
                    if line == "\n":
                        post["content"].append(paragraph)
                        paragraph = {"text": "", "type": 0}
                    else:
                        paragraph["text"] += line.rstrip("\n")
                    doc += line.rstrip("\n") + " "
                post["content"].append(paragraph)

                post["readtime"] = round(len(doc.split()) / 275)
                post["preview"] = doc[0:100]

                posts.append(post)
    return sorted(posts, key=lambda x: x["date"], reverse=True)


posts = load_posts()


@app.route("/")
def home():
    return render_template("home.html", posts = posts)


@app.route("/<year>/<month>/<day>/<title>")
def post(year, month, day, title):
    for post in posts:
        if post["title"] == title and post["date"] == datetime(int(year), int(month), int(day)):
            return render_template("post.html", post = post)

if __name__ == "__main__":
    app.run()