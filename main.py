import sys
import time
import requests
import worker

from PyQt5.QtCore import Qt, QThread
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
		
		layout.addWidget(QLabel("Select files:"))
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
		self.uploadButton.clicked.connect(self.uploadFile)
		
		# Handle upload
		# self.obj = worker.Worker()
		# self.thread = QThread()
		# self.obj.intReady.connect(self.onIntReady)


	def getFiles(self):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		if dlg.exec_():
			self.filenames.append(dlg.selectedFiles())
			self.contents.setText(self.filenames[-1][0])
			self.filesList.addItems(self.filenames[-1])

	def uploadFile(self):
		print("Upload button clicked")
		url = "http://localhost:5000/upload"
		uploadData = {
			'file': self.filenames[-1][0]
		}
		r = requests.post(url, files = uploadData)

		# for file in self.filenames:
		# 	print(file[0])
		# 	self.progBar.setValue(100)

# App
login = LoginScreen()

if login.exec_() == QDialog.Accepted:
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())

