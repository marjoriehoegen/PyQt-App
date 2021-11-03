from flask import Flask, request, Response
from werkzeug.datastructures import FileStorage
import os

app = Flask(__name__)

# Function to handle login
@app.route('/login',methods = ['POST'])
def loginHandler():
	username = request.form['username']
	password = request.form['password']
	if username == 'username' and password == 'password':
		return "200"
	else:
		return Response("Login error", status=401)

# Function to upload files
@app.route('/upload', methods=['POST'])
def uploadFiles():
	
	# Path to save the files
	dir_path = os.path.dirname(os.path.realpath(__file__))
	upload_dest = os.path.join(dir_path,'uploads')

	if request.method == 'POST':
		files = request.files['file']

		for file in files:
			with open(file, 'rb') as fp:
				file = FileStorage(fp)
				path_to_save = os.path.join(upload_dest, os.path.basename(file.filename))
				file.save(path_to_save)
		return "ok"


if __name__ == '__main__':
	app.run(debug=True)