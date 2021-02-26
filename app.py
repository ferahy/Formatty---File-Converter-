from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import templates

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Tuse/Formatty---File-Converter-/database_files/filestorage.sqlite3'
db = SQLAlchemy(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    #data = db.Column(db.LargeBinary)
    
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']

    newFile = FileContents(name=file.filename)
    #, data=file.read())
    db.session.add(newFile)
    db.session.commit()

    return 'Saved ' + file.filename + ' to the database'


if __name__ == "__main__":
    db.drop_all
    db.create_all