import sys
import time
import requests
import os


from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QListWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout

app = QApplication(sys.argv)

# Login screen
class LoginScreen(QDialog):
	"""
	Definition of the login screen.
	"""
	def __init__(self):
		super().__init__()
		
		# Create layout
		layout = QVBoxLayout()
		self.setWindowTitle('Login')
		self.username = QLineEdit('username')
		self.password = QLineEdit('password')
		self.password.setEchoMode(QLineEdit.Password)
		self.loginButton = QPushButton('Login')

		layout.addWidget(QLabel('Username:'))
		layout.addWidget(self.username)
		layout.addWidget(QLabel('Password:'))
		layout.addWidget(self.password)
		layout.addWidget(self.loginButton)

		self.setLayout(layout)
		
		# Button to handle login
		self.loginButton.clicked.connect(self.handleLogin)


	# Function to handle login
	def handleLogin(self, checked):
		url = "http://localhost:5000/login"		
		loginData = {
			'username': self.username.text(),
			'password': self.password.text()
		}
		r = requests.get(url, data = loginData)

		if r.status_code == 200:
			print("Login successul!")
			self.accept()
		else:
			QMessageBox.warning(self, 'Error', 'Wrong username or password')

# Main screen
class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Main Application')
		self.resize(800,600)

		# Files list
		filesLayout = QGridLayout()
		
		self.filenames = []
		self.filesList = QListWidget()
		filesLayout.addWidget(self.filesList, 1, 0, 1, 2)
		QListWidget.setFixedWidth(self.filesList,400)

		# Upload section
		layout = QVBoxLayout()

		self.selectFileBtn = QPushButton("Open")
		self.uploadButton = QPushButton("Upload")
		self.cancelButton = QPushButton("Cancel")
		self.progBar = QProgressBar()
		self.contents = QTextEdit()
		
		layout.addWidget(QLabel("Select file:"))
		layout.addWidget(self.selectFileBtn)
		layout.addWidget(self.contents)
		layout.addWidget(self.uploadButton)
		layout.addWidget(self.cancelButton)
		layout.addWidget(self.progBar)

		# Main layout
		outerLayout = QHBoxLayout()
		outerLayout.addLayout(filesLayout)
		outerLayout.addLayout(layout)
		self.setLayout(outerLayout)

		# Configure buttons
		self.selectFileBtn.clicked.connect(self.getFiles)

		self.thread = UploadThread(filenames=self.filenames)
		self.uploadButton.clicked.connect(self.uploadFile)

		self.cancelButton.clicked.connect(self.cancelUpload)


	def getFiles(self):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		if dlg.exec_():
			self.filenames.append(dlg.selectedFiles())
			self.contents.setText(self.filenames[-1][0])
			self.filesList.addItems(self.filenames[-1])

	def uploadFile(self):
		self.thread.start()
		# self.thread.progressChanged.connect(self.progBar.setValue)
		
	# def updateProgressBar(self):
	# 	print("Update progress bar")

		# self.progBar.setValue(val)

		# for i in range(maxVal):
		# 	self.progBar.setValue(self.progBar.value() + 1)
		# 	time.sleep(1)
		# 	maxVal = maxVal - 1
		# 	if maxVal == 0:
		# 		self.progBar.setValue(100)

	def cancelUpload(self):
		print("Cancel upload button clicked")
		self.thread.terminate()
		self.progBar.setValue(0)

class UploadThread(QThread):
	# progressChanged = pyqtSignal(int)
	
	def __init__(self, filenames, parent=None):
		QThread.__init__(self, parent)
		self.filenames = filenames	

	def run(self):

		print("Thread started")
		url = "http://localhost:5000/upload"
		fileToUpload = self.filenames[-1][0]
		
		# print(os.path.getsize(fileToUpload))

		uploadData = {
			'file': fileToUpload
		}			
		r = requests.post(url, files = uploadData)

		# progressbar_value = 0
		# while progressbar_value < 100:
		# 	print(progressbar_value)
		# 	self.progressChanged.emit(progressbar_value)
		# 	time.sleep(0.1)
		# 	progressbar_value += 1

		# val = int(100 * monitor.bytes_read / monitor.len)

# App
login = LoginScreen()

if login.exec_() == QDialog.Accepted:
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())

