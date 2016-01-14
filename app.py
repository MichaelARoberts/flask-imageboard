from flask import Flask,render_template,request,redirect,url_for,flash
from werkzeug import secure_filename
import os
import models

#Folder to save all images to
UPLOAD_FOLDER = './static/images'

#File extensions users can upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#Counts the number of files we have.
#TODO remove this and just count database entries eventually.
file_count = int();

#Flask app setup
app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Creating database tables
models.create_tables()

#determines if users can upload files
#TODO move to a utility script later
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#Home Page
@app.route("/")
def home():
    image_locations = list()

    for image in models.Image.select():
        image_locations.append(image.image_location)

    return render_template("index.html", image_locations = image_locations)

#Submission Page
@app.route("/submit", methods=["GET","POST"])
def submit():
    global file_count

    # Recalulate how many images their are each time we submit, and adjust
    path = './static/images/'
    file_count = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])

    if request.method == "POST":
        new_image_name = request.form["image_name_input"]
        file = request.files['image_upload']
        file_ext = file.filename.split(".")[1]

        try:
            # changing the filename to amount of files we have, plus the extension
            filename = secure_filename(str(file_count) + "." + file_ext)

            if file and allowed_file(file.filename):
                #Save the image to the server
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                #Creating a database entry, with the location of the image
                models.Image.create(image_name=str(new_image_name), image_location = filename)

                flash("<|>Your Image as been added!")

            elif file and not allowed_file(file.filename):
                flash("<!>That image type is not accepted.")

        except:
            flash("<!>That Image name already exsists.")

    return render_template("submit.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
