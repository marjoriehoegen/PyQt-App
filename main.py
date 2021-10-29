import sys
import time

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout

app = QApplication(sys.argv)


# tela de login
# usuário e senha

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
		
	# def showMainWindow(self, checked):
	# 	if self.w is None:
	# 		self.w = MainWindow()
	# 		self.w.show()

	# 	else:
	# 		self.w.close()  # Close window.
	# 		self.w = None  # Discard reference.


	# Function to handle login
	def handleLogin(self, checked):
		if (self.username.text() == "username" and self.password.text() == "password"):
			print("Login successul!")
			self.accept()
		else:
			QMessageBox.warning(self, 'Error', 'Wrong username or password')

# implementar servidor

# tela principal
# botão para seleção do arquivo
# botão para upload do arquivo
# área para: lista de arquivos sendo feito o upload, a barra de progresso e uma previsão de término
# opção para cancelar o upload

# class MainWindow(QMainWindow):
class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Main Application')

		# Select files to upload
		self.selectFileBtn = QPushButton("Open")
		self.uploadButton = QPushButton("Begin upload")
		
		layout = QHBoxLayout()
		layout.addWidget(QLabel("Select files:"))
		layout.addWidget(self.selectFileBtn)
		layout.addWidget(self.uploadButton)

		# Upload status

		self.thread = QThread()
		
		self.contents = QTextEdit()
		self.cancelButton = QPushButton("Cancel")
		self.progBar = QProgressBar()

		uploadLayout = QGridLayout()
		uploadLayout.addWidget(QLabel("File name"), 0, 0)
		uploadLayout.addWidget(QLabel("Upload progress"), 0, 1)
		uploadLayout.addWidget(QLabel("Cancel upload"), 0, 2)

		uploadLayout.addWidget(self.contents, 1, 0)
		uploadLayout.addWidget(self.progBar, 1, 1)
		uploadLayout.addWidget(self.cancelButton, 1, 2)
		
		outerLayout = QVBoxLayout()
		outerLayout.addLayout(layout)
		outerLayout.addLayout(uploadLayout)

		self.setLayout(outerLayout)

		# Direct buttons
		self.selectFileBtn.clicked.connect(self.getFiles)
		self.filenames = []
		self.uploadButton.clicked.connect(self.uploadFile)


	def getFiles(self):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		# dlg.setFilter("Text files (*.txt)")
		if dlg.exec_():
			self.filenames.append(dlg.selectedFiles())
			self.contents.append(self.filenames[-1][0])		

	def uploadFile(self):
		print("Upload button clicked")
	
		for file in self.filenames:
			print(file[0])
			self.progBar.setValue(100)

		
# implementar servidor upload

login = LoginScreen()

if login.exec_() == QDialog.Accepted:
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())

# O aplicativo deverá estar sempre disponível no trackbar do windows (mesmo quando o aplicativo for fechado pela janela principal)
# deverá haver um menu no trackbar do windows com a possibilidade de fechar o aplicativo

# arquivo de dependências `requirements.txt` com as dependências utilizadas
# código com um arquivo README.md com as instruções de execução

# sys.exit(app.exec_())