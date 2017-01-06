

from flask import Flask,render_template,redirect,url_for,request
import mongoengine
from mongoengine import *
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#mongodb://<dbuser>:<dbpassword>@ds133328.mlab.com:33328/vuhoang98

host ="ds133328.mlab.com"
port= 33328
db_name ="vuhoang98"
user_name = "admin"
password = "141298"

mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

class User(Document):
    songname = StringField()
    artists = StringField()
    image = StringField()
    link = StringField()

unit = []
unit_2 = []

@app.route('/')
def index():
    return render_template("upload.html")

images_folder = os.path.join(APP_ROOT, 'static/images/')
@app.route('/upload',methods=["POST"])
def upload():
    #images_folder = os.path.join(APP_ROOT, 'static/images/')
    #print(images_folder)

    if not os.path.isdir(images_folder) : #neu folder chua duoc khoi tao
        os.mkdir(images_folder) #mkdir = make directory

    for image in request.files.getlist('file') :
        image_name = image.filename
        print(' ',image_name)
        image_dir = "/".join([images_folder,image_name]) #join lấy 1 list
        print(image_dir)
        # thêm một đối tượng vào cơ sở dữ liệu
        image.save(image_dir)
    unit.append(User(image= image_name, songname="1", artists="2", link="3"))
    user= User(image= image_name, songname="1", artists="2", link="3")
    user.save()

    return render_template("loadimage.html", unit=unit)



@app.route("/music")
def music():
    return render_template("Music.html",music_list= User.objects)

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/addmore",methods=["GET","POST"])
def addmore():
    if request.method =="GET" :
        return render_template("addmore.html")
    elif request.method == "POST":
        songnamex = request.form["songname"]
        artistsx = request.form["artists"]
        linkx = request.form["link"]
        for image in request.files.getlist('file'):
            imagex = "/".join([images_folder,image.filename])
        print(imagex)
        user = User(songname= songnamex, artists= artistsx,image = imagex, link=linkx)
        user.save()
        return redirect(url_for("thankyou"))

@app.route("/delete/<string:id>")
def delete(id):
    user = User.objects().with_id(id)
    if user is not None:
        user.delete()
        return render_template("thankyou.html")
    elif user is None:
        return ("not found")

@app.route("/update/<string:id>",methods=["GET","POST"])
def update(id):
    user = User.objects().with_id(id)
    if request.method =="GET" :
        return render_template("update.html", id = id)
    elif request.method == "POST":
        if request.form["yourname"] != "" :
            user.update(set__yourname=request.form["yourname"])
        if request.form["songname"] != "":
            user.update(set__songname =request.form["songname"])
        if request.form["artists"] != "":
            user.update(set__artists=request.form["artists"])
        if request.form["image"] != "":
            user.update(set__image=request.form["image"])
        if request.form["link"] != "":
            user.update(set__link=request.form["link"])
        return render_template("thankyou.html")

@app.route("/edit")
def edit():
    return render_template("edit.html",music_list=User.objects)

@app.route('/profile')
def profile():
    return render_template("profile.html")
if __name__ == '__main__':
  app.run()

