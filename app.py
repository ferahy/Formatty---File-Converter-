from flask import Flask, request, render_template, flash, redirect, send_file, url_for, session
from flask_sqlalchemy import SQLAlchemy
import templates
#from app.forms import LoginForm
from io import BytesIO
# docx to pdf
from docx2pdf import convert
# png to pdf 
import img2pdf
from PIL import Image
import os
import sys
# pdf to docx 
from pdf2docx import Converter

#Used to PATH formatting

from pdf2image import convert_from_path
import glob


app = Flask(__name__)

#Database Formatting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filestorage.sqlite3'
UPLOAD_FOLDER = 'tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.pdf', '.docx']
db = SQLAlchemy(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    data_pdf = db.Column(db.LargeBinary)
    data_png = db.Column(db.LargeBinary)
    data_docx = db.Column(db.LargeBinary)

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    

#All Flask APP routes
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        data = User.query.filter_by(username=name, password=passw).first()
        if data is not None:
            session['logged_in'] = True
            return render_template('home.html')
        else:
            return render_template('home.html', message="Incorrect Details")
        

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return render_template('home.html')
        except:
            return render_template('login.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], (file.filename)))
    #Checks if the file format is acceptabe
    VALID_FORMATS = {"pdf", "PNG", "docx", "jpg"}
    valid = 0
    for valid_format in VALID_FORMATS:
        if (file.filename)[-len(valid_format):] == valid_format:
            newFile = FileContents(name=file.filename[:-len(valid_format)-1], data=file.read())
            valid = 1
            original_format = valid_format
            break
    if valid == 0:
        return "Error: Wrong Format."

    
    #TODO: Implement convert logic
    newFile.data_pdf = newFile.data
    #newFile.data_png = newFile.data
    #newFile.data_docx = newFile.data

    #Need to upload newFile.data to the folder TMP
    

    #------------convert starts here-----------

    if original_format == "pdf":
        

        outputDir = "tmp/"
        input_path = "tmp/" + newFile.name + ".pdf"
        pages = convert_from_path(input_path, 500)
        img = pages[0]

        # Create a buffer to hold the bytes
        buf = BytesIO()

        # Save the image as jpeg to the buffer
        img.save(buf, 'jpeg')

        # Rewind the buffer's file pointer
        buf.seek(0)

        # Read the bytes from the buffer
        image_bytes = buf.read()

        # Close the buffer
        buf.close()

        #Upload file to DB
        newFile.data_png = image_bytes
        
        
       

  


    db.session.add(newFile)
    db.session.commit()
    return redirect('/download/' + str(newFile.id))


@app.route('/download')
def download():
    return render_template('download_main.html')

@app.route('/download1', methods = ['POST'])
def download1():
    input_id = request.form['input_id']
    return redirect('/download/' + str(input_id))

@app.route('/download/<int:file_id>')
def download_main_page(file_id):
    #This page should have all 3 boxes for "download pdf" , "download png"
    # "download docx", and a "Copy link box, that when clicked, will copy
    #The url to the clipboard
    file_data = FileContents.query.filter_by(id=file_id).first()
    if file_data == None:
            return "Error there is no file with that ID"

    return render_template('download.html', name = file_data.name, file_id = file_id)

@app.route('/download/<string:file_type>/<int:file_id>')
def download_file(file_type, file_id):
    file_data = FileContents.query.filter_by(id=file_id).first()

    if file_type == "pdf":
        format_data = file_data.data_pdf
    elif file_type == "png":
        format_data = file_data.data_png
    elif file_type == "docx":
        format_data = file_data.data_png

    converted_filename = file_data.name + "." + file_type

    return send_file(BytesIO(format_data), attachment_filename = converted_filename, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    db.create_all()
