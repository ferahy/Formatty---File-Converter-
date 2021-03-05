from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import templates

app = Flask(__name__)

#Database Formatting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filestorage.sqlite3'
db = SQLAlchemy(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

#All Flask APP routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']

    newFile = FileContents(name=file.filename, data=file.read())
    #db.add_file(newFile)
    db.session.add(newFile)
    db.session.commit()

    return 'Saved ' + file.filename + ' to the database'
