import sys
import io
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QComboBox, QPushButton, QSlider, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QBuffer, Qt, QByteArray
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageQt import ImageQt
from pathlib import Path

'''
 Programa que nos ayuda a poner filtros básicos a imágenes, usando PyQt para crear la interfaz gráfica. (La cual es muy básica)
 Hecho por Jonathan Suárez López.
 # Cuenta: 313259595
'''
class Filtros(QWidget):
	def __init__(self):
		super().__init__()

		self.title = "Filtros PDI by Jonayne."
		self.left = 10
		self.top = 10
		self.width = 1280
		self.height = 720
		self.initUI()

	#Iniciamos todos los elementos y los acomodamos.
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.line_edit_n = QLineEdit(self)
		self.line_edit_m = QLineEdit(self)

		self.line_edit_m.move(410, 694)
		self.line_edit_n.move(540, 694)
		self.line_edit_n.close()
		self.line_edit_m.close()

		self.lbl_mos = QLabel("Escriba la región deseada (n x m)", self)
		self.lbl_mos.move(420, 677)
		self.lbl_mos.close()

		self.slider = QSlider(Qt.Horizontal, self)
		self.slider.setFocusPolicy(Qt.StrongFocus)
		self.slider.setTickPosition(QSlider.TicksBelow)
		self.slider.setTickInterval(10)
		self.slider.setSingleStep(1)
		self.slider.setGeometry(450, 690, 200, 20)
		self.slider.setMaximum(127)
		self.slider.setMinimum(-127)
		self.slider.setValue(0)

		self.lbl_bri = QLabel("Escoja la cantidad a aumentar o disminuir el brillo.", self)
		self.lbl_bri.move(450, 677)
		self.lbl_bri.close()
		self.slider.close()

		self.input = QLineEdit(self)
		self.input.move(540, 694)

		self.lbl_text = QLabel("Escriba el texto que quiera mostrar", self)
		self.lbl_text.move(450, 677)
		self.lbl_text.close()
		self.input.close()

		self.label_img_ori = QLabel(self)
		self.label_img_fil = QLabel(self)
		self.label_img_ori.setGeometry(QtCore.QRect(5, 28, 610, 650))
		self.label_img_fil.setGeometry(QtCore.QRect(630, 28, 610, 650))

		self.label_img_ori.setScaledContents(True)
		self.label_img_fil.setScaledContents(True)

		self.lbl_esco = QLabel("Escoja el filtro que quiere aplicar.", self)
		self.lbl_esco.move(25, 680)

		self.button_cargar = QPushButton('Cargar Imagen', self)
		self.button_cargar.setToolTip('Selecciona una imagen para editar.')
		self.button_cargar.move(1,1)

		self.button_cargar.clicked.connect(self.cargar_imagen)

		self.button_guardar = QPushButton('Guardar Imagen', self)
		self.button_guardar.setToolTip('Guarde la imagen con filtro aplicado.')
		self.button_guardar.move(150, 1)

		self.button_guardar.clicked.connect(self.guardar_imagen)

		self.button_aplicar = QPushButton('Aplicar: Quitar marca de agua', self)
		self.button_aplicar.setToolTip('Aplique el filtro que escogió.')
		self.button_aplicar.move(230,690)

		self.filtro_escogido = "Quitar marca de agua" #El que está por default.

		self.button_aplicar.clicked.connect(self.aplica_filtro)

		self.combo = QComboBox(self)

		# Lista de filtros.
		self.combo.addItem("Quitar marca de agua")
		self.combo.addItem("Brillo")
		self.combo.addItem("Mosaico")
		self.combo.addItem("Inverso")
		self.combo.addItem("Alto contraste")
		self.combo.addItem("Blur")
		self.combo.addItem("Motion Blur")
		self.combo.addItem("Encontrar bordes")
		self.combo.addItem("Sharpen")
		self.combo.addItem("Emboss")
		self.combo.addItem("Mediana")
		self.combo.addItem("Letra a color")
		self.combo.addItem("Letra tono de gris")
		self.combo.addItem("Letras blanco y negro")
		self.combo.addItem("Letras en color")
		self.combo.addItem("Texto definido")
		self.combo.addItem("Naipes")
		self.combo.addItem("Domino")
		self.combo.addItem("Tono de gris 1")
		self.combo.addItem("Tono de gris 2")
		self.combo.addItem("Tono de gris 3")
		self.combo.addItem("Tono de gris 4")
		self.combo.addItem("Tono de gris 5")
		self.combo.addItem("Tono de gris 6")
		self.combo.addItem("Tono de gris 7")
		self.combo.addItem("Tono de gris 8")

		self.combo.move(25, 690)

		self.combo.activated[str].connect(self.onActivated)
		
		self.show()

	'''
		Método que carga una imagen en el programa y la muestra.
	'''
	@pyqtSlot()
	def cargar_imagen(self):
		try:
			image = QFileDialog.getOpenFileName(self,'Open File','~/')
			imagePath = image[0]
			self.pixmap_ori = QPixmap(imagePath).scaled(610, 650, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
			self.pixmap_fil = QPixmap(imagePath).scaled(610, 650, Qt.KeepAspectRatio, Qt.SmoothTransformation)

			self.label_img_ori.setPixmap(self.pixmap_ori)

			#Para poder modificarla con PIL.
			img = QImage(imagePath)
			buffer = QBuffer()
			buffer.open(QBuffer.ReadWrite)
			img.save(buffer, Path(imagePath).suffix[1:])
			self.pil_im_or = Image.open(io.BytesIO(buffer.data())) 
			self.label_img_fil.setPixmap(QPixmap())
		except Exception:
			print("Error de lectura de archivo.")


	'''
		Método que guarda la imagen actual fitrada.
	'''
	@pyqtSlot()
	def guardar_imagen(self):
		try:
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()","",'Sólo en PNG (*.png)', options=options)
			if file_name:
				
				pixmap = self.pixmap_fil

				# Save QPixmap to QByteArray via QBuffer.
				byte_array = QByteArray()
				buffer = QBuffer(byte_array)
				buffer.open(QBuffer.ReadWrite)
				pixmap.save(buffer, Path(file_name).suffix[1:])

				with open(file_name, 'wb') as out_file:
					out_file.write(byte_array)

		except Exception:
			print("Error de lectura/escritura de archivo.")

	'''
		Método que cambia algunos Widgets al escoger un filtro en el combo.
	'''
	def onActivated(self, text):
		self.filtro_escogido = text
		self.button_aplicar.setText("Aplicar " + text)
		self.button_aplicar.adjustSize()
		if text == "Brillo":
			self.slider.show()
			self.lbl_bri.show()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.lbl_text.close()
			self.input.close()
		elif text == "Mosaico":
			self.lbl_mos.show()
			self.line_edit_n.show()
			self.line_edit_m.show()
			self.slider.close()
			self.lbl_bri.close()
			self.lbl_text.close()
			self.input.close()
		elif text == "Texto definido":
			self.lbl_text.show()
			self.input.show()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.slider.close()
			self.lbl_bri.close()			
		else:
			self.slider.close()
			self.lbl_bri.close()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.lbl_text.close()
			self.input.close()

	'''
		Método que según un filtro fijado, lo aplica a la imagen cargada en el programa.
	'''
	@pyqtSlot()
	def aplica_filtro(self):

		filtro = self.filtro_escogido

		if filtro == "Tono de gris 1":
			img = self.tono_gris1(self.pil_im_or.copy())
		elif filtro == "Tono de gris 2":
			img = self.tono_gris2(self.pil_im_or.copy())
		elif filtro == "Tono de gris 3":
			img = self.tono_gris3(self.pil_im_or.copy())
		elif filtro == "Tono de gris 4":
			img = self.tono_gris4(self.pil_im_or.copy())
		elif filtro == "Tono de gris 5":
			img = self.tono_gris5(self.pil_im_or.copy())
		elif filtro == "Tono de gris 6":
			img = self.tono_gris6(self.pil_im_or.copy())
		elif filtro == "Tono de gris 7":
			img = self.tono_gris7(self.pil_im_or.copy())
		elif filtro == "Tono de gris 8":
			img = self.tono_gris8(self.pil_im_or.copy())
		elif filtro == "Brillo":
			img = self.brillo(self.pil_im_or.copy(), self.slider.value())
		elif filtro == "Mosaico":
			img = self.mosaico(self.pil_im_or.copy(), int(self.line_edit_n.text()), int(self.line_edit_m.text()))
		elif filtro == "Inverso":
			img = self.inverso(self.pil_im_or.copy())
		elif filtro == "Alto contraste":
			img = self.alto_contraste(self.pil_im_or.copy())
		elif filtro == "Blur":
			img = self.blur(self.pil_im_or.copy())
		elif filtro == "Motion Blur":
			img = self.motion_blur(self.pil_im_or.copy())
		elif filtro == "Encontrar bordes":
			img = self.edges(self.pil_im_or.copy())
		elif filtro == "Sharpen":
			img = self.sharpen(self.pil_im_or.copy())
		elif filtro == "Emboss":
			img = self.emboss(self.pil_im_or.copy())
		elif filtro == "Mediana":
			img = self.mediana(self.pil_im_or.copy())
		elif filtro == "Letra a color":
			img = self.letra_color(self.pil_im_or.copy())
		elif filtro == "Letra tono de gris":
			img = self.letra_tono_gris(self.pil_im_or.copy())
		elif filtro == "Letras blanco y negro":
			img = self.letras_bn(self.pil_im_or.copy())
		elif filtro == "Letras en color":
			img = self.letras_c(self.pil_im_or.copy())
		elif filtro == "Texto definido":
			img = self.texto_def(self.pil_im_or.copy(), self.input.text())
		elif filtro == "Naipes":
			img = self.naipes(self.pil_im_or.copy())
		elif filtro == "Domino":
			img = self.domino(self.pil_im_or.copy())
		elif filtro == "Quitar marca de agua":
			img = self.quitar_marca(self.pil_im_or.copy())
		img.show()
		self.pixmap_fil = self.dame_pixmap(img)
		self.label_img_fil.setPixmap(self.pixmap_fil)
		self.label_img_fil.repaint()




	def dame_pixmap(self, img):
		qim = ImageQt(img)
		pix = QPixmap.fromImage(qim)
		return pix

	def tono_gris1(self, img):
		pixels = img.load() #Creamos el mapa de pixeles.
		for i in range(img.size[0]):    #columnas:
			for j in range(img.size[1]):    #renglones
				#Obtenemos el gris:
				gris = int(rojo(pixels[i,j]) * 0.3 + verde(pixels[i,j]) * 0.59 + azul(pixels[i,j]) * 0.11)
				pixels[i,j] = (gris, gris, gris) #ponemos el nuevo color.
		return img
		

	def tono_gris2(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):    
				#Obtenemos el gris:
				gris = (rojo(pixels[i,j]) + verde(pixels[i,j]) + azul(pixels[i,j]))//3
				pixels[i,j] = (gris, gris, gris) #ponemos el nuevo color.
		return img
		
		

	def tono_gris3(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):   
				#Obtenemos el gris:
				maximo = max(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
				minimo = min(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
				gris = (maximo + minimo)//2
				pixels[i,j] = (gris, gris, gris) #ponemos el nuevo color.
		return img
		
		

	def tono_gris4(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):    
				#Obtenemos el gris:
				gris = max(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
				pixels[i,j] = (gris, gris, gris) #ponemos el nuevo color.
		return img
		

	def tono_gris5(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):    
				#Obtenemos el gris:
				gris = min(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
				pixels[i,j] = (gris, gris, gris) #ponemos el nuevo color.
		
		return img

	def tono_gris6(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):    
				pixels[i,j] = (rojo(pixels[i,j]), rojo(pixels[i,j]), rojo(pixels[i,j])) #ponemos el nuevo color.
		return img
		

	def tono_gris7(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):    
				pixels[i,j] = (verde(pixels[i,j]), verde(pixels[i,j]), verde(pixels[i,j])) #ponemos el nuevo color.
		return img
		
		
	def tono_gris8(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):   
			for j in range(img.size[1]):    
				pixels[i,j] = (azul(pixels[i,j]), azul(pixels[i,j]), azul(pixels[i,j])) #ponemos el nuevo color.
		return img
		
		
	def brillo(self, img, cte):
		pixels = img.load() 
		for i in range(img.size[0]):   
			for j in range(img.size[1]):    
				pixels[i,j] = (azul(pixels[i,j]) + cte, 
				azul(pixels[i,j]) + cte, 
				azul(pixels[i,j]) + cte)
		return img
		
		
	def mosaico(self, img, n, m):
		pixels = img.load() 
		for i in range(img.size[0]):    
			for j in range(img.size[1]):    
				if i % n == 0 and j % m == 0 and i != 0 and j != 0:
					promedio = self.saca_promedio(pixels, i, j, n, m)
					for x in range(i-n, i):
						for y in range(j-m, j):
							pixels[x,y] = (promedio[0], promedio[1], promedio[2]) #ponemos el nuevo color.
		return img
		
		
	def inverso(self, img):
		pixels = img.load() 
		for i in range(img.size[0]):   
			for j in range(img.size[1]):    
				pixels[i,j] = ((rojo(pixels[i,j]) - 255) * (-1), 
					(verde(pixels[i,j]) - 255) * (-1), 
					(azul(pixels[i,j]) - 255) * (-1)) 
		return img
		
	
	def saca_promedio(self, pixels, i, j, n, m):
		sumaR = 0
		sumaV = 0
		sumaA = 0
		for x in range(i-n, i):
			for y in range(j-m, j):
				sumaR += rojo(pixels[x,y])
				sumaV += verde(pixels[x,y]) 
				sumaA += azul(pixels[x,y])
		return [sumaR//(n*m), sumaV//(n*m), sumaA//(n*m)]

	def alto_contraste(self, img):
		img = self.tono_gris1(img)
		pixels = img.load()

		for i in range(img.size[0]):    
			for j in range(img.size[1]):
				if rojo(pixels[i,j]) > 127:
					n_rojo = 255
				else:
					n_rojo = 0
				if verde(pixels[i,j]) > 127:
					n_verde = 255
				else:
					n_verde = 0
				if azul(pixels[i,j]) > 127:
					n_azul = 255
				else:
					n_azul = 0	

				pixels[i,j] = (n_rojo, n_verde, n_azul)

		return img
		

	def blur(self, img):
		pixels = img.load() 
		for i in range(2, img.size[0]):   
			for j in range(2, img.size[1]):
				try:
					n_rojo = (rojo(pixels[i, j-2])
					+ rojo(pixels[i-1, j-1]) + rojo(pixels[i, j-1]) + rojo(pixels[i+1, j-1]) 
					+ rojo(pixels[i-2, j]) + rojo(pixels[i-1, j]) + rojo(pixels[i, j]) + rojo(pixels[i+1, j]) + rojo(pixels[i+2, j]) 
					+ rojo(pixels[i-1, j+1]) + rojo(pixels[i, j+1]) + rojo(pixels[i+1, j+1])
					+ rojo(pixels[i, j+2]))//13
					if n_rojo > 255:
						n_rojo = 255
					if n_rojo < 0:
						n_rojo = 0
					n_verde = (verde(pixels[i, j-2])
					+ verde(pixels[i-1, j-1]) + verde(pixels[i, j-1]) + verde(pixels[i+1, j-1]) 
					+ verde(pixels[i-2, j]) + verde(pixels[i-1, j]) + verde(pixels[i, j]) + verde(pixels[i+1, j]) + verde(pixels[i+2, j]) 
					+ verde(pixels[i-1, j+1]) + verde(pixels[i, j+1]) + verde(pixels[i+1, j+1])
					+ verde(pixels[i, j+2]))//13
					if n_verde > 255:
						n_verde = 255
					if n_verde < 0:
						n_verde = 0
					n_azul = (azul(pixels[i, j-2])
					+ azul(pixels[i-1, j-1]) + azul(pixels[i, j-1]) + azul(pixels[i+1, j-1]) 
					+ azul(pixels[i-2, j]) + azul(pixels[i-1, j]) + azul(pixels[i, j]) + azul(pixels[i+1, j]) + azul(pixels[i+2, j]) 
					+ azul(pixels[i-1, j+1]) + azul(pixels[i, j+1]) + azul(pixels[i+1, j+1])
					+ azul(pixels[i, j+2]))//13
					if n_azul > 255:
						n_azul = 255
					if n_azul < 0:
						n_azul = 0
					pixels[i,j] = (n_rojo, n_verde, n_azul)
				except Exception:
					pixels[i, j] = pixels[i, j]
		return img
		


	def motion_blur(self, img):
		pixels = img.load() 
		for i in range(2, img.size[0]):   
			for j in range(2, img.size[1]):
				try:
					n_rojo = (rojo(pixels[i-2, j-2]) + rojo(pixels[i-1, j-1]) + rojo(pixels[i, j]) 
						+ rojo(pixels[i+1, j+1]) + rojo(pixels[i+2, j+2]))//5
					if n_rojo > 255:
						n_rojo = 255
					if n_rojo < 0:
						n_rojo = 0
					n_verde = (verde(pixels[i-2, j-2]) + verde(pixels[i-1, j-1]) + verde(pixels[i, j]) 
						+ verde(pixels[i+1, j+1]) + verde(pixels[i+2, j+2]))//5
					if n_verde > 255:
						n_verde = 255
					if n_verde < 0:
						n_verde = 0
					n_azul = (azul(pixels[i-2, j-2]) + azul(pixels[i-1, j-1]) + azul(pixels[i, j]) 
						+ azul(pixels[i+1, j+1]) + azul(pixels[i+2, j+2]))//5
					if n_azul > 255:
						n_azul = 255
					if n_azul < 0:
						n_azul = 0
					pixels[i,j] = (n_rojo, n_verde, n_azul)
				except Exception:
					pixels[i, j] = pixels[i, j]
		return img
		

	def edges(self, img):
		pixels = img.load() 
		for i in range(2, img.size[0]):   
			for j in range(2, img.size[1]):
				try:
					n_rojo = ((rojo(pixels[i-2, j-2]) * (-1)) + (rojo(pixels[i-1, j-1]) * (-2)) + (rojo(pixels[i, j]) * (6)) 
						+ (rojo(pixels[i+1, j+1]) * (-2)) + (rojo(pixels[i+2, j+2]) * (-1)))
					if n_rojo > 255:
						n_rojo = 255
					if n_rojo < 0:
						n_rojo = 0
					n_verde = ((verde(pixels[i-2, j-2]) * (-1)) + (verde(pixels[i-1, j-1]) * (-2)) + (verde(pixels[i, j]) * (6)) 
						+ (verde(pixels[i+1, j+1]) * (-2)) + (verde(pixels[i+2, j+2]) * (-1)))
					if n_verde > 255:
						n_verde = 255
					if n_verde < 0:
						n_verde = 0
					n_azul = ((azul(pixels[i-2, j-2]) * (-1)) + (azul(pixels[i-1, j-1]) * (-2)) + (azul(pixels[i, j]) * (6)) 
						+ (azul(pixels[i+1, j+1]) * (-2)) + (azul(pixels[i+2, j+2]) * (-1)))
					if n_azul > 255:
						n_azul = 255
					if n_azul < 0:
						n_azul = 0
					pixels[i,j] = (n_rojo, n_verde, n_azul)
				except Exception:
					pixels[i, j] = pixels[i, j]
		return img
		

	def sharpen(self, img):
		pixels = img.load() 
		for i in range(1, img.size[0]):   
			for j in range(1, img.size[1]):
				try:
					n_rojo = ((rojo(pixels[i-1, j-1]) * (-1)) + (rojo(pixels[i, j-1]) * (-1)) + (rojo(pixels[i+1, j-1]) * (-1))
						+ (rojo(pixels[i-1, j]) * (-1)) + (rojo(pixels[i, j]) * 9) + (rojo(pixels[i+1, j]) * (-1))
						+ (rojo(pixels[i-1, j+1]) * (-1)) + (rojo(pixels[i, j+1]) * (-1)) + (rojo(pixels[i+1, j+1]) * (-1)))
					if n_rojo > 255:
						n_rojo = 255
					if n_rojo < 0:
						n_rojo = 0
					n_verde = ((verde(pixels[i-1, j-1]) * (-1)) + (verde(pixels[i, j-1]) * (-1)) + (verde(pixels[i+1, j-1]) * (-1))
						+ (verde(pixels[i-1, j]) * (-1)) + (verde(pixels[i, j]) * 9) + (verde(pixels[i+1, j]) * (-1))
						+ (verde(pixels[i-1, j+1]) * (-1)) + (verde(pixels[i, j+1]) * (-1)) + (verde(pixels[i+1, j+1]) * (-1)))
					if n_verde > 255:
						n_verde = 255
					if n_verde < 0:
						n_verde = 0
					n_azul = ((azul(pixels[i-1, j-1]) * (-1)) + (azul(pixels[i, j-1]) * (-1)) + (azul(pixels[i+1, j-1]) * (-1))
						+ (azul(pixels[i-1, j]) * (-1)) + (azul(pixels[i, j]) * 9) + (azul(pixels[i+1, j]) * (-1))
						+ (azul(pixels[i-1, j+1]) * (-1)) + (azul(pixels[i, j+1]) * (-1)) + (azul(pixels[i+1, j+1]) * (-1)))
					if n_azul > 255:
						n_azul = 255
					if n_azul < 0:
						n_azul = 0

					pixels[i,j] = (n_rojo, n_verde, n_azul)
				except Exception:
					pixels[i, j] = pixels[i, j]
		return img				

	def emboss(self, img):
		pixels = img.load() 
		for i in range(1, img.size[0]):   
			for j in range(1, img.size[1]):
				try:
					n_rojo = ((rojo(pixels[i-1, j-1]) * (-1)) + (rojo(pixels[i, j-1]) * (-1))
						+ (rojo(pixels[i-1, j]) * (-1)) + rojo(pixels[i+1, j]) + rojo(pixels[i, j+1]) + rojo(pixels[i+1, j+1]))
					if n_rojo > 255:
						n_rojo = 255
					if n_rojo < 0:
						n_rojo = 0
					n_verde = ((verde(pixels[i-1, j-1]) * (-1)) + (verde(pixels[i, j-1]) * (-1))
						+ (verde(pixels[i-1, j]) * (-1)) + verde(pixels[i+1, j]) + verde(pixels[i, j+1]) + verde(pixels[i+1, j+1]))
					if n_verde > 255:
						n_verde = 255
					if n_verde < 0:
						n_verde = 0
					n_azul = ((azul(pixels[i-1, j-1]) * (-1)) + (azul(pixels[i, j-1]) * (-1)) + (azul(pixels[i-1, j]) * (-1)) 
						+ azul(pixels[i+1, j]) + azul(pixels[i, j+1]) + azul(pixels[i+1, j+1]))
					if n_azul > 255:
						n_azul = 255
					if n_azul < 0:
						n_azul = 0

					pixels[i,j] = (n_rojo, n_verde, n_azul)
				except Exception:
					pixels[i, j] = pixels[i, j]
		return img

	def mediana(self, img):
		pixels = img.load() 
		for i in range(1, img.size[0]):   
			for j in range(1, img.size[1]):
				try:
					m = 9//2
					n_rojo = [rojo(pixels[i-1, j-1]), rojo(pixels[i, j-1]), rojo(pixels[i+1, j-1])
						 ,rojo(pixels[i-1, j]),  rojo(pixels[i, j]), rojo(pixels[i+1, j])
						 ,rojo(pixels[i-1, j+1]), rojo(pixels[i, j+1]), rojo(pixels[i+1, j+1])]
					n_rojo.sort()
					n_verde = [verde(pixels[i-1, j-1]), verde(pixels[i, j-1]), verde(pixels[i+1, j-1])
						 ,verde(pixels[i-1, j]),  verde(pixels[i, j]), verde(pixels[i+1, j])
						 ,verde(pixels[i-1, j+1]), verde(pixels[i, j+1]), verde(pixels[i+1, j+1])]
					n_verde.sort()
					n_azul = [azul(pixels[i-1, j-1]), azul(pixels[i, j-1]), azul(pixels[i+1, j-1])
						 ,azul(pixels[i-1, j]),  azul(pixels[i, j]), azul(pixels[i+1, j])
						 ,azul(pixels[i-1, j+1]), azul(pixels[i, j+1]), azul(pixels[i+1, j+1])]
					n_azul.sort()

					pixels[i,j] = (n_rojo[m], n_verde[m], n_azul[m])

				except Exception:
					pixels[i, j] = pixels[i, j]
		return img

	def letra_color(self, img):
		n=8
		m=8
		mosaico = self.mosaico(img, n, m)
		pixels = mosaico.load()
		rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		draw = ImageDraw.Draw(rejilla)
		font = ImageFont.truetype("fonts/courbd.ttf", 10)
		for i in range(0, mosaico.size[0], 8):
			for j in range(0, mosaico.size[1], 8):
				draw.text((i, j), "X", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
		
		
		return rejilla
		
	def letra_tono_gris(self, img):
		n=8
		m=8
		tono_gris = self.tono_gris1(img)
		mosaico = self.mosaico(tono_gris, n, m)

		pixels = mosaico.load()
		rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		draw = ImageDraw.Draw(rejilla)
		font = ImageFont.truetype("fonts/courbd.ttf", 10)
		for i in range(0, mosaico.size[0], 8):
			for j in range(0, mosaico.size[1], 8):
				draw.text((i, j), "X", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
		
		
		return rejilla

	def letras_bn(self, img):
		n=8
		m=8
		tgris = self.tono_gris1(img)
		mosaico = self.mosaico(tgris, n, m)

		pixels = mosaico.load()
		rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		draw = ImageDraw.Draw(rejilla)
		font = ImageFont.truetype("fonts/courbd.ttf", 10)
		for i in range(0, mosaico.size[0], 8):
			for j in range(0, mosaico.size[1], 8):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 16): 
					draw.text((i, j), "M", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 16 and prom < 32): 
					draw.text((i, j), "N", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 32 and prom < 48): 
					draw.text((i, j), "H", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 48 and prom < 64): 
					draw.text((i, j), "#", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 64 and prom < 80): 
					draw.text((i, j), "Q", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 80 and prom < 96): 
					draw.text((i, j), "U", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 96 and prom < 112): 
					draw.text((i, j), "A", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 112 and prom < 128): 
					draw.text((i, j), "D", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 128 and prom < 144): 
					draw.text((i, j), "O", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 144 and prom < 160): 
					draw.text((i, j), "Y", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 160 and prom < 176): 
					draw.text((i, j), "2", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 176 and prom < 192): 
					draw.text((i, j), "$", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 192 and prom < 208): 
					draw.text((i, j), "%", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 208 and prom < 224): 
					draw.text((i, j), "+", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 224 and prom < 240): 
					draw.text((i, j), "_", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 240 and prom < 256): 
					draw.text((i, j), " ", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)

		
		return rejilla

	def letras_c(self, img):
		n=8
		m=8

		mosaico = self.mosaico(img, n, m)

		pixels = mosaico.load()
		rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		draw = ImageDraw.Draw(rejilla)
		font = ImageFont.truetype("fonts/courbd.ttf", 10)
		for i in range(0, mosaico.size[0], 8):
			for j in range(0, mosaico.size[1], 8):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 16): 
					draw.text((i, j), "M", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 16 and prom < 32): 
					draw.text((i, j), "N", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 32 and prom < 48): 
					draw.text((i, j), "H", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 48 and prom < 64): 
					draw.text((i, j), "#", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 64 and prom < 80): 
					draw.text((i, j), "Q", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 80 and prom < 96): 
					draw.text((i, j), "U", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 96 and prom < 112): 
					draw.text((i, j), "A", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 112 and prom < 128): 
					draw.text((i, j), "D", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 128 and prom < 144): 
					draw.text((i, j), "O", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 144 and prom < 160): 
					draw.text((i, j), "Y", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 160 and prom < 176): 
					draw.text((i, j), "2", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 176 and prom < 192): 
					draw.text((i, j), "$", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 192 and prom < 208): 
					draw.text((i, j), "%", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 208 and prom < 224): 
					draw.text((i, j), "+", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 224 and prom < 240): 
					draw.text((i, j), "_", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 240 and prom < 256): 
					draw.text((i, j), " ", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
		
		
		return rejilla


	def texto_def(self, img, cad):
		try:
			n=8
			m=8
			mosaico = self.mosaico(img.copy(), n, m)
			pixels = mosaico.load()
			rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
			draw = ImageDraw.Draw(rejilla)
			font = ImageFont.truetype("fonts/courbd.ttf", 10)
			for i in range(0, mosaico.size[0], (len(cad) * 6) ):
				for j in range(0, mosaico.size[1], 8):
					draw.text((i, j), cad, (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
			
			
			return rejilla
		except Exception:
			print("ERROR! Escoja entrada válida.")
			return img

	def naipes(self, img):
		n=8
		m=8

		mosaico = self.mosaico(img, n, m)

		pixels = mosaico.load()
		rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		draw = ImageDraw.Draw(rejilla)
		font = ImageFont.truetype("fonts/PLAYCRDS.TTF", 13)
		for i in range(0, mosaico.size[0], 10):
			for j in range(0, mosaico.size[1], 10):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 23): 
					draw.text((i, j), "Z", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 23 and prom < 46): 
					draw.text((i, j), "W", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 46 and prom < 69): 
					draw.text((i, j), "V", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 69 and prom < 92): 
					draw.text((i, j), "U", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 92 and prom < 115): 
					draw.text((i, j), "T", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 115 and prom < 138): 
					draw.text((i, j), "S", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 138 and prom < 161): 
					draw.text((i, j), "R", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 161 and prom < 184): 
					draw.text((i, j), "Q", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 184 and prom < 207): 
					draw.text((i, j), "P", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 207 and prom < 230): 
					draw.text((i, j), "O", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 230 and prom < 256): 
					draw.text((i, j), "N", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
		
		
		return rejilla

	def domino(self, img):
		n=8
		m=8

		mosaico = self.mosaico(img, n, m)

		pixels = mosaico.load()
		rejilla = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		draw = ImageDraw.Draw(rejilla)
		font = ImageFont.truetype("fonts/Lasvbld_.ttf", 10)
		for i in range(0, mosaico.size[0], 8):
			for j in range(0, mosaico.size[1], 8):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 37): 
					draw.text((i, j), "6", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 37 and prom < 74): 
					draw.text((i, j), "5", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 74 and prom < 111): 
					draw.text((i, j), "4", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 111 and prom < 148): 
					draw.text((i, j), "3", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 148 and prom < 185): 
					draw.text((i, j), "2", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 185 and prom < 222): 
					draw.text((i, j), "1", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
				elif(prom >= 222 and prom < 256): 
					draw.text((i, j), "0", (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])), font=font)
		
				
		return rejilla

	def quitar_marca(self, img):
		pixels = img.load()
		# Quitamos la marca de agua de las partes en las que choca con lo que no es blanco. 
		for i in range(img.size[0]):    
			for j in range(img.size[1]): 
				if(not es_gris(pixels[i,j])):
					if(rojo(pixels[i,j]) > verde(pixels[i,j]) and rojo(pixels[i,j]) > azul(pixels[i,j])):
						pixels[i,j] = (rojo(pixels[i,j]), rojo(pixels[i,j]), rojo(pixels[i,j]))
					elif(verde(pixels[i,j]) > azul(pixels[i,j])):
						pixels[i,j] = (verde(pixels[i,j]), verde(pixels[i,j]), verde(pixels[i,j]))  
					else:
						pixels[i,j] = (azul(pixels[i,j]), azul(pixels[i,j]), azul(pixels[i,j]))
				else:
					pixels[i,j] = (rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j])) #ponemos el nuevo color.
		mosaico = self.mosaico(img, 1, 2)
		pixels2 = mosaico.load()
		# Hacemos un efecto pequeño de mosaico y obtenemos color promedio intentando quitar la marca de agua.
		for i in range(0, mosaico.size[0]):
			for j in range(0, mosaico.size[1]):
				prom = ((rojo(pixels2[i, j]) + verde(pixels2[i, j]) + azul(pixels2[i, j]))/3)
				if (prom >= 206.5):
					pixels2[i,j] = (255,255,255)
				else:
					pixels2[i,j] = (rojo(pixels2[i,j]), verde(pixels2[i,j]), azul(pixels2[i,j]))

		return mosaico

def es_gris(pixel):
	if(rojo(pixel) == verde(pixel) and rojo(pixel) == azul(pixel) and azul(pixel) == verde(pixel)):
		return True
	else:
		return False

#Nos sirve para obtener el componente rojo de un pixel.
def rojo(pixel):
	return pixel[0]

#Nos sirve para obtener el componente verde de un pixel.
def verde(pixel):
	return pixel[1]

#Nos sirve para obtener el componente azul de un pixel.
def azul(pixel):
	return pixel[2]

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Filtros()
	sys.exit(app.exec_())
