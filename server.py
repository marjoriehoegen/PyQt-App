from flask import Flask, request
from werkzeug.datastructures import FileStorage
import os

app = Flask(__name__)

# Function to handle login
@app.route('/login',methods = ['GET', 'POST'])
def loginHandler():
	if request.method == 'GET' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		if username != 'username' and password != 'password':
			return 200
		else:
			return "Error"
	else:
		return "Error"

# Function to upload files
@app.route('/upload', methods=['POST'])
def uploadFiles():
	# Path to save the files
	dir_path = os.path.dirname(os.path.realpath(__file__))
	upload_dest = os.path.join(dir_path,'uploads')
	print(upload_dest)

	if request.method == 'POST':
		# files = request.files.getlist('filenames')

		# até aqui ok
		files = request.files['file']
		# files = request.files.get('file')
		
		print(files)
		print("ok")

		for file in files:
			print("entered for loop")
			print(file)

			with open(file, 'rb') as fp:
				file = FileStorage(fp)
				path_to_save = os.path.join(upload_dest, os.path.basename(file.filename))
				file.save(path_to_save)
			print("saved")

		return "ok"


		# return redirect('/upload')



if __name__ == '__main__':
	app.run(debug=True)