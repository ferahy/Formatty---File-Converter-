from flask import Flask, request, render_template, flash, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import templates
#from app.forms import LoginForm
from io import BytesIO


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

@app.route("/file_list")
def file_list():

    #
    database = FileContents.query.all()
    return render_template('file_list.html', data = database)

   
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
    
    #newFile = FileContents(name=file.filename, data=file.read())
    
    #TODO: Implement convert logic
    newFile.data_pdf = file.read()
    newFile.data_png = file.read()
    newFile.data_docx = file.read()
    
    db.session.add(newFile)
    db.session.commit()
    
    
    return render_template('download.html', name = newFile.name, file_id = newFile.id)
   

@app.route('/download/<string:file_type>/<int:file_id>')
def download(file_type, file_id):
    file_data = FileContents.query.filter_by(id=file_id).first()

    if file_type == "pdf":
        format_data = file_data.data_pdf
    elif file_type == "png":
        format_data = file_data.data_png
    elif file_type == "docx":
        format_data = file_data.data_png
    
    converted_filename = file_data.name + "." + file_type

    return send_file(BytesIO(format_data), attachment_filename = converted_filename, as_attachment=True)
