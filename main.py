import os
from datetime import datetime
from flask import Flask, render_template

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

                img_count = 0
                for line in rf:
                    paragraph = {"text": "", "type": "br"}
                    line = line.lstrip().rstrip()
                    if line[:3] == "<p>":
                        paragraph["text"] += line[3:]
                        paragraph["type"] = "p"
                    elif line[:4] == "<h1>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "h1"
                    elif line[:4] == "<h2>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "h2"
                    elif line[:4] == "<h3>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "h3"
                    elif line[:4] == "<h4>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "h4"
                    elif line[:4] == "<h5>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "h5"
                    elif line[:4] == "<h6>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "h6"
                    elif line[:4] == "<li>":
                        paragraph["text"] += line[4:]
                        paragraph["type"] = "li"
                    if line[:3] == "img":
                        paragraph["text"] += "post-images/" + file.rstrip(".txt") + "-" + str(img_count) + line[4:]
                        paragraph["type"] = "img"
                        img_count += 1
                    else:
                        doc += paragraph["text"] + " "
                    post["content"].append(paragraph)
                post["readtime"] = round((len(doc.split()) + 12 * img_count) / 240)
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
