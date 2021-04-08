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
    #data_pdf = db.Column(db.LargeBinary)
    #data_png = db.Column(db.LargeBinary)
    #data_jpg = db.Column(db.LargeBinary)

#All Flask APP routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/file_list")
def file_list():
    database = FileContents.query.all()
    return render_template('file_list.html', data = database)

   
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']

    #Checks if the file format is acceptabe
    VALID_FORMATS = {"pdf", "png", "doc"}
    valid = 0
    for valid_format in VALID_FORMATS:
        if (file.filename)[-3:] == valid_format:
            valid = 1
    if valid == 0:
        return "Error: Wrong Format."
    
    newFile = FileContents(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()
    
    
    return render_template('download.html', name = newFile.name, file_id = newFile.id)
    #return 'Saved' + file.filename + ' to the database'
    

@app.route('/download/<string:file_type>/<int:file_id>')
def download(file_type, file_id):
    file_data = FileContents.query.filter_by(id=file_id).first()



    return send_file(BytesIO(file_data.data), attachment_filename = file_data.name, as_attachment=True)
    

