import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QFileDialog, QStatusBar, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout

app = QApplication(sys.argv)


# tela de login
# usuário e senha

class LoginScreen(QWidget):
	"""
	Definition of the login screen.
	"""
	def __init__(self):
		super().__init__()
		self.w = None

		# Create layout
		layout = QVBoxLayout()
		self.username = QLineEdit('username')
		self.password = QLineEdit('password')
		self.password.setEchoMode(QLineEdit.Password)
		self.loginButton = QPushButton('Login')

		layout.addWidget(self.username)
		layout.addWidget(self.password)
		layout.addWidget(self.loginButton)

		self.setLayout(layout)
		
		# Button to login and go to main window
		self.loginButton.clicked.connect(self.showMainWindow)
		
	def showMainWindow(self, checked):
		if self.w is None:
			self.w = MainWindow()
			self.w.show()

		else:
			self.w.close()  # Close window.
			self.w = None  # Discard reference.

# tela principal
# botão para seleção do arquivo
# botão para upload do arquivo
# área para: lista de arquivos sendo feito o upload, a barra de progresso e uma previsão de término
# opção para cancelar o upload

# class MainWindow(QMainWindow):
class MainWindow(QWidget):

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()

		self.welcomeMsg = QLabel('Hello!')		
		self.uploadButton = QPushButton("Select file to upload ")
		self.contents = QTextEdit() # filenames

		layout.addWidget(self.welcomeMsg)
		layout.addWidget(self.uploadButton)
		layout.addWidget(self.contents)
		
		self.setLayout(layout)

		# Select file
		self.uploadButton.clicked.connect(self.getfiles)

	def getfiles(self):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		# dlg.setFilter("Text files (*.txt)")
		filenames = []
	
		if dlg.exec_():
			filenames = dlg.selectedFiles()
			self.contents.setText(filenames[0])
			
			# f = open(filenames[0], 'r')
			# with f:
			# 	data = f.read()
			# 	self.contents.setText(data)


w = LoginScreen()
w.show()

# O aplicativo deverá estar sempre disponível no trackbar do windows (mesmo quando o aplicativo for fechado pela janela principal)
# deverá haver um menu no trackbar do windows com a possibilidade de fechar o aplicativo

# arquivo de dependências `requirements.txt` com as dependências utilizadas
# código com um arquivo README.md com as instruções de execução

sys.exit(app.exec_())