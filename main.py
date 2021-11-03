import sys
import time
import requests

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QListWidget, QSystemTrayIcon, QMenu, QAction
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
		r = requests.post(url, data = loginData)
		print(r.status_code)

		if r.status_code == 200:
			self.accept()
		else:
			QMessageBox.warning(self, 'Error', 'Wrong username or password')

# Main screen
class MainWindow(QWidget):
	"""
	Definition of main screen to select and upload files.
	"""

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
		# self.progBar = QProgressBar()
		self.contents = QTextEdit()
		
		layout.addWidget(QLabel("Select file:"))
		layout.addWidget(self.selectFileBtn)
		layout.addWidget(self.contents)
		layout.addWidget(self.uploadButton)
		layout.addWidget(self.cancelButton)
		# layout.addWidget(self.progBar)

		# Main layout
		outerLayout = QHBoxLayout()
		outerLayout.addLayout(filesLayout)
		outerLayout.addLayout(layout)
		self.setLayout(outerLayout)

		# Configure system tray
		self.closeEvent = self.onClose
		self.systemTray = QSystemTrayIcon()
		self.systemTray.setContextMenu(QMenu(self))

		self.tray = QSystemTrayIcon(QIcon("icon.png"), self)
		self.trayMenu = QMenu(self)

		actionShowWindow = QAction("Show main window", self)
		actionShowWindow.triggered.connect(self.onShowMainWindow)
		self.trayMenu.addAction(actionShowWindow)

		actionExit = QAction("Exit", self)
		actionExit.triggered.connect(app.exit)
		self.trayMenu.addAction(actionExit)

		self.tray.setContextMenu(self.trayMenu)
		self.tray.activated.connect(self.onTrayActivated)
		self.tray.show()

		# Configure buttons
		self.selectFileBtn.clicked.connect(self.getFiles)
		self.thread = UploadThread(filenames=self.filenames)
		self.uploadButton.clicked.connect(self.uploadFile)
		self.cancelButton.clicked.connect(self.cancelUpload)


	# System tray functions
	def onClose(self, event):
		self.tray.show()

	def onShowMainWindow(self):
		self.show()
		self.tray.hide()

	def onTrayActivated(self, event: QSystemTrayIcon.ActivationReason):
		if event == QSystemTrayIcon.ActivationReason.Trigger:
			self.onShowMainWindow()

	# Functions to manage upload actions
	def getFiles(self):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		if dlg.exec_():
			self.filenames.append(dlg.selectedFiles())
			self.contents.setText(self.filenames[-1][0])
			self.filesList.addItems(self.filenames[-1])

	def uploadFile(self):
		self.thread.start()

	def cancelUpload(self):
		self.thread.terminate()

class UploadThread(QThread):
	"""
	Definition of upload thread.
	"""

	def __init__(self, filenames, parent=None):
		QThread.__init__(self, parent)
		self.filenames = filenames	

	def run(self):
		url = "http://localhost:5000/upload"
		fileToUpload = self.filenames[-1][0]
		uploadData = {
			'file': fileToUpload
		}			
		r = requests.post(url, files = uploadData)

# App

login = LoginScreen()

app.setQuitOnLastWindowClosed(False)

if login.exec_() == QDialog.Accepted:
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())

