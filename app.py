from flask import Flask, render_template, request, redirect, escape, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
import os
from werkzeug.utils import secure_filename
from os.path import exists

#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER']                  = os.path.join(app.instance_path, 'uploads')
app.config['MAX_CONTENT_LENGTH']             = 10 * 1000 * 1000 # limit uploads to 10 megabytes

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

Base = declarative_base()


class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column('location_id', db.Integer, primary_key = True)
    latitude    = db.Column(db.Float(), default=0.0)
    longitude   = db.Column(db.Float(), default=0.0)
    address     = db.Column(db.String(200), default="unkown")
    note        = db.Column(db.String(200), default="none")
    file        = db.Column(db.String(50), default="none")
    extension   = db.Column(db.String(50), default="none")
    deleted     = db.Column('deleted', db.Integer, default=0)

    def __init__(self, latitude, longitude, address, note, file, extension, deleted):
        self.latitude  = latitude
        self.longitude = longitude
        self.address   = address
        self.note      = note
        self.file      = file
        self.extension = extension
        self.deleted   = deleted


db.session.commit()
    
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_latitude(latitude):
    try:
        if (latitude >= -90) and (latitude <= 90):
            return round(latitude,7)
        else:
            return 0.0
    except:
        return render_template('error.html', msg="Invalid Latitude")

def sanitize_longitude(longitude):
    try:
        longitude = (longitude % 360 + 540) % 360 - 180.0
        return round(longitude,7)
    except:
        return render_template('error.html', msg="Invalid Longitude")

def add_record(record):
    try:
        db.session.add(record)
        db.session.commit()
        return True
    except:
        return False

@app.route("/", methods=["GET", "POST"])
def home():
    db.create_all()
    locations = Location.query.all()
    if locations != []:
        return render_template('home.html', flag=True, locations=locations)
    else:
        return render_template('home.html', flag=False)

@app.route("/<float(signed=True):lat>/<float(signed=True):long>/<float(signed=True):zoom>", methods=["GET", "POST"])
def home_loc(lat, long, zoom):
    db.create_all()
    locations = Location.query.all()
    if locations != []:
        return render_template('home.html', flag=True, locations=locations, lat=lat, long=long, zoom=zoom)
    else:
        return render_template('home.html', flag=False)
    
@app.route("/location/create/", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        try:
            latitude, longitude  = request.form.get('latlong').split(",", maxsplit=1)
            latitude  = sanitize_latitude( float( latitude ) )
            longitude = sanitize_longitude( float( longitude ) )
            address   = escape(request.form.get('address')) if request.form.get('address') else "unkown"
            note      = escape(request.form.get('note')) if request.form.get('note') else "none"
            filename = "none"
            extension = "none"
            # print(request.__dict__)
            if 'file' in request.files:
                print("File in request")
                file = request.files['file']
                if file.filename == '':
                    print('No selected file')
                else:
                    filename  = secure_filename(file.filename) # save original filename to DB
                    extension = '.' in filename and filename.rsplit('.', 1)[1].lower()
                    print("File selected: " + filename)
                    if allowed_file(filename) and not exists(os.path.join(app.config['UPLOAD_FOLDER'], filename) ):
                        newfilename = str(latitude) + str(longitude) + "." + extension
                        print("Allowed extension AND file doesn't exist, saving to:" + os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename)) # save file to disk using location as filename
                    else:
                        print("Unknown file extension or file already exist")
            else:
                print('No file')

            record = Location(latitude, longitude, address, note, filename, extension, 0)
            status = add_record(record)
        except Exception as e:
            return render_template('error.html', msg="Error creating location: " + getattr(e, 'message', repr(e)))
    return redirect("/" + str(latitude) + "/" + str(longitude) + "/" + str(request.form.get('zoom') ) )

@app.route('/location/<int:location_id>/update/', methods=["GET", "POST"])
def update(location_id):
    try:
        location = Location.query.filter_by(location_id=location_id).first()
        if request.method == "GET":
            return render_template('update.html', location=location)
        elif request.method == "POST":
            latitude, longitude  = request.form.get('latlong').split(",", maxsplit=1)
            location.latitude  = sanitize_latitude( float( latitude ) )
            location.longitude = sanitize_longitude( float( longitude ) )
            print("lat:" + str(location.latitude) + " long:" + str(location.longitude) + " zoom:" + str(request.form.get('zoom') ) )
            # location.address = request.form.get('address']
            location.note = escape(request.form.get('note') )
            if 'file' in request.files:
                print("File in request")
                file = request.files['file']
                if file.filename == '':
                    print('No selected file')
                else:
                    filename  = secure_filename(file.filename) # save original filename to DB
                    extension = '.' in filename and filename.rsplit('.', 1)[1].lower()
                    print("File selected: " + filename)
                    if allowed_file(filename) and not exists(os.path.join(app.config['UPLOAD_FOLDER'], filename) ):
                        newfilename = str(location.latitude) + str(location.longitude) + "." + extension
                        print("Allowed extension AND file doesn't exist, saving to:" + os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename)) # save file to disk using location as filename
                        location.file = filename
                        location.extension = extension
                    else:
                        print("Unknown file extension or file already exist")
            else:
                print('No file')
            db.session.commit()
    except Exception as e:
        return render_template('error.html', msg="Error updating location: " + getattr(e, 'message', repr(e)))
    finally:
        print("redirecting to: " + ("/" + str(location.latitude) + "/" + str(location.longitude) + "/" + str(request.form.get('zoom') ) ) )
        return redirect("/" + str(location.latitude) + "/" + str(location.longitude) + "/" + str(request.form.get('zoom') ) )


@app.route('/location/<int:location_id>/delete/', methods=["GET", "POST"])
def delete(location_id):
    if request.method == "GET":
        location = Location.query.get_or_404(location_id)
        try:
            location.deleted = 1
            db.session.commit()
        except Exception as e:
            return render_template('error.html', msg="Error deleting location: " + getattr(e, 'message', repr(e)))
        finally:
            return redirect("/")


@app.route('/location/<int:location_id>/', methods=["GET", "POST"])
def personal(location_id):

    location = Location.query.filter_by(location_id=location_id).first()
    if request.method == "GET":
        return render_template('personal_details.html', location=location)

@app.route('/uploads/<path:filename>')
def custom_static(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return render_template('error.html', msg="Error deleting location: " + getattr(e, 'message', repr(e)))

if __name__ == '__main__':
    app.run(port=5001)