import sys
import io
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QBuffer, Qt, QByteArray
from PIL import Image, ImageStat
from PIL.ImageQt import ImageQt
from pathlib import Path

'''
 Programa que crea un archivo de texto con información sobre cierta cantidad de imágenes.
 Hecho por Jonathan Suárez López.
 # Cuenta: 313259595
'''
class Info_imgs(QWidget):
	def __init__(self):
		super().__init__()

		self.title = "Creador de información de paquete de imágenes."
		self.left = 10
		self.top = 10
		self.width = 400
		self.height = 200
		self.initUI()

	#Iniciamos todos los elementos y los acomodamos.
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.lbl_name = QLabel("Escriba el nombre del archivo que se creará.", self)
		self.lbl_name.move(60, 10)
		self.nombre_arc = QLineEdit(self)
		self.nombre_arc.move(60,30)

		self.button_cargar = QPushButton('Cargar y operar conjunto de imágenes', self)
		self.button_cargar.setToolTip('Selecciona una carpeta de imágenes.')
		self.button_cargar.move(60,100)

		self.button_cargar.clicked.connect(self.cargar_paquete)
		
		self.show()

	'''
		Método que carga un paquete de imágenes y obtiene información de ellas para el fotomosaico posterior.
	'''
	@pyqtSlot()
	def cargar_paquete(self):
		try:
			f = open(self.nombre_arc.text()+".txt", "w+")
			file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
			# Los for son para viajar por todo el directorio de imágenes que escogimos y crear el archivo de texto.
			for root, dirs, files in os.walk(file):
				for d in dirs:
					img = Image.open(os.path.abspath(os.path.join(root, d)))
					rgb_prom = tuple(ImageStat.Stat(img).median)
					# El if es para asegurarnos que rgb_prom sea una tripleta.
					if(len(rgb_prom) == 3):
						#Escribimos en el archivo de texto y separamos cada cosa con un /.
						f.write(str(rgb_prom[0]) + "/" + str(rgb_prom[1]) + "/"  + str(rgb_prom[2]) + "/" + os.path.abspath(os.path.join(root, d)) + "\n")
			for fi in files:
				img = Image.open(os.path.abspath(os.path.join(root, fi)))
				rgb_prom = tuple(ImageStat.Stat(img).median)
				if(len(rgb_prom) == 3):
					f.write(str(rgb_prom[0]) + "/" + str(rgb_prom[1]) + "/"  + str(rgb_prom[2]) + "/" + os.path.abspath(os.path.join(root, fi)) + "\n")
		
			f.close()
			print("¡Se han terminado de procesar!")
		except IOError:
			print("Error de lectura de archivo.")

		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Info_imgs()
	sys.exit(app.exec_())
