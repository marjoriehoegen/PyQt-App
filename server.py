from flask import Flask, request
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
	# path definition to save the file
	dir_path = os.path.dirname(os.path.realpath(__file__))
	upload_dest = os.path.join(dir_path,'uploads')

	if request.method == 'POST':
		# files = request.files.getlist('filenames')
		files = request.files['file']
		print(files)
		print("ok")

		for file in files:
			print("entered for loop")
			print(file)
			file.save(os.path.join(upload_dest, file.filename))
			print("saved")

		return "ok"


		# return redirect('/upload')



if __name__ == '__main__':
	app.run(debug=True)