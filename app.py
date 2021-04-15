from flask import Flask, request, render_template, flash, redirect, send_file
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
# pdf to docx 
from pdf2docx import Converter


app = Flask(__name__)

#Database Formatting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filestorage.sqlite3'
db = SQLAlchemy(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    data_pdf = db.Column(db.LargeBinary)
    data_png = db.Column(db.LargeBinary)
    data_docx = db.Column(db.LargeBinary)

#All Flask APP routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']

    #Checks if the file format is acceptabe
    VALID_FORMATS = {"pdf", "png", "docx"}
    valid = 0
    for valid_format in VALID_FORMATS:
        if (file.filename)[-len(valid_format):] == valid_format:
            newFile = FileContents(name=file.filename[:-len(valid_format)-1], data=file.read())
            valid = 1
            break
    if valid == 0:
        return "Error: Wrong Format."


    #TODO: Implement convert logic
    newFile.data_pdf = newFile.data
    newFile.data_png = newFile.data
    newFile.data_docx = newFile.data
    #------------convert starts here-----------

    # pdf to docx  

    # docx to pdf
    if (file.filename)[-len(valid_format):] == 'docx':
        convert(newFile.data_docx)
        convert('/download/' + str(newFile.id), '/download/' + str(newFile.id))
        convert("/download/")

    # png to pdf
    #image = Image.open(r'newFile.data_png')
    #image1 = image.convert('RGB')
    #image1.save(r'/download/'+ str(newFile.id))

    #--------------------------------------------

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
