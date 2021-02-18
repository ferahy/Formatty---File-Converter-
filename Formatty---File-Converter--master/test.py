from flask import Flask, request, render_template
import templates

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def say_hello():
		text = request.form['text']
		return "Hello " + text + "!"
