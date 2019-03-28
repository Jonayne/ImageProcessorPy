import sys
import io
import math
import random
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

		self.line_edit_m.move(440, 694)
		self.line_edit_n.move(570, 694)
		self.line_edit_n.close()
		self.line_edit_m.close()

		self.lbl_mos = QLabel("Escriba la región deseada (n x m)", self)
		self.lbl_mos.move(450, 677)
		self.lbl_mos.close()

		self.colores_paquete = []
		self.imgs_paquete = []

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

		self.path_fotomosaico = None

		self.input = QLineEdit(self)
		self.input.move(540, 694)

		self.lbl_text = QLabel("Escriba el texto que quiera mostrar", self)
		self.lbl_text.move(450, 677)
		self.lbl_text.close()
		self.input.close()

		self.lbl_text_luz = QLabel("Escriba el peso (de 1 a 7)", self)
		self.lbl_text_luz.move(450, 677)
		self.lbl_text_luz.close()

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

		self.button_cargar_mos = QPushButton('Cargar conjunto de imágenes', self)
		self.button_cargar_mos.setToolTip('Selecciona una carpeta de imágenes.')
		self.button_cargar_mos.move(400,690)

		self.button_cargar_mos.clicked.connect(self.cargar_paquete)
		self.button_cargar_mos.close()

		self.colores_r = [(0,0,255), (255,255,255), (255,255,0), (0,128,0), (255,165,0), (255,0,0), (220,209,43), (220, 43, 220), (43, 49, 220), (149, 66, 50), (75, 49, 202), (6, 97, 12), (0, 0, 0), (176, 42, 225), (220, 43, 220), (42, 225, 200), (28, 37, 36), (84, 58, 64)]
		self.button_guardar = QPushButton('Guardar Imagen', self)
		self.button_guardar.setToolTip('Guarde la imagen con filtro aplicado.')
		self.button_guardar.move(150, 1)

		self.button_guardar.clicked.connect(self.guardar_imagen)

		self.button_aplicar = QPushButton('Aplicar...', self)
		self.button_aplicar.setToolTip('Aplique el filtro que escogió.')
		self.button_aplicar.move(230,690)

		self.filtro_escogido = ""
		self.num_colors_rubik = "256 colores" #rubik

		self.button_aplicar.clicked.connect(self.aplica_filtro)

		self.combo_rubik = QComboBox(self)
		self.combo_rubik.addItem("256 colores")
		self.combo_rubik.addItem("18 colores")
		self.combo_rubik.close()

		self.combo_rubik.activated[str].connect(self.onActivated_r) #rubik

		self.combo_rubik.move(400, 694)

		self.combo = QComboBox(self)

		# Lista de filtros.
		self.combo.addItem("Escoja un filtro")
		self.combo.addItem("Fotomosaico")
		self.combo.addItem("Random Dithering")
		self.combo.addItem("Rubik")
		self.combo.addItem("Recursiva /C")
		self.combo.addItem("Recursiva /T")				
		self.combo.addItem("Luz negra")		
		self.combo.addItem("AT&T")
		self.combo.addItem("Ecualizar imagen")
		self.combo.addItem("Semitonos A")
		self.combo.addItem("Semitonos B")
		self.combo.addItem("Semitonos C")
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
			self.pil_im_or = self.dame_img_PIL(imagePath)
			self.label_img_fil.setPixmap(QPixmap())
		except Exception:
			print("Error de lectura de archivo.")

	'''
		Método que carga un paquete de imágenes y obtiene información de ellas para el fotomosaico posterior.
	'''
	@pyqtSlot()
	def cargar_paquete(self):
		try:
			self.path_fotomosaico = QFileDialog.getOpenFileName(self, 'Open File', '~/', 'txt(*.txt)')
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
			self.lbl_text_luz.close()
			self.combo_rubik.close()
			self.button_cargar_mos.close()
		elif text == "Mosaico" or text == "Semitonos A" or text == "Semitonos A" or text == "Semitonos B" or text == "Semitonos C" or text == "Recursiva /C" or text == "Recursiva /T":
			self.lbl_mos.show()
			self.line_edit_n.show()
			self.line_edit_m.show()
			self.slider.close()
			self.lbl_bri.close()
			self.lbl_text.close()
			self.input.close()
			self.lbl_text_luz.close()
			self.combo_rubik.close()
			self.button_cargar_mos.close()
		elif text == "Texto definido":
			self.lbl_text.show()
			self.input.show()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.slider.close()
			self.lbl_bri.close()
			self.lbl_text_luz.close()
			self.combo_rubik.close()
			self.button_cargar_mos.close()
		elif text == "Luz negra":
			self.lbl_text_luz.show()
			self.lbl_text.close()
			self.input.show()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.slider.close()
			self.lbl_bri.close()
			self.combo_rubik.close()
			self.button_cargar_mos.close()
		elif text == "Rubik":
			self.lbl_text_luz.close()
			self.lbl_text.close()
			self.input.close()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.slider.close()
			self.lbl_bri.close()
			self.combo_rubik.show()
			self.button_cargar_mos.close()
		elif text == "Fotomosaico":
			self.lbl_text_luz.close()
			self.lbl_text.close()
			self.input.close()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.slider.close()
			self.lbl_bri.close()
			self.combo_rubik.close()
			self.button_cargar_mos.show()
		else:
			self.slider.close()
			self.lbl_bri.close()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()
			self.lbl_text.close()
			self.input.close()
			self.lbl_text_luz.close()
			self.combo_rubik.close()
			self.button_cargar_mos.close()

	def onActivated_r(self, text): #rubik
		self.num_colors_rubik = text #rubik

	'''
		Método que según un filtro fijado, lo aplica a la imagen cargada en el programa.
	'''
	@pyqtSlot()
	def aplica_filtro(self):
		#try:
		filtro = self.filtro_escogido
		if filtro != "":
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
			elif filtro == "Ecualizar imagen":
				img = self.ecualizar_img(self.pil_im_or.copy())
			elif filtro == "Semitonos A":
				img = self.semitonosA(self.pil_im_or.copy(), int(self.line_edit_n.text()), int(self.line_edit_m.text()))
			elif filtro == "Semitonos B":
				img = self.semitonosB(self.pil_im_or.copy(), int(self.line_edit_n.text()), int(self.line_edit_m.text()))
			elif filtro == "Semitonos C":
				img = self.semitonosC(self.pil_im_or.copy(), int(self.line_edit_n.text()), int(self.line_edit_m.text()))
			elif filtro == "Luz negra":
				img = self.luz_negra(self.pil_im_or.copy(), int(self.input.text()))
			elif filtro == "AT&T":
				img = self.at_t(self.pil_im_or.copy())
			elif filtro == "Recursiva /C":
				img = self.recursiva_c(self.pil_im_or.copy(), int(self.line_edit_n.text()), int(self.line_edit_m.text()))
			elif filtro == "Recursiva /T":
				img = self.recursiva_b(self.pil_im_or.copy(), int(self.line_edit_n.text()), int(self.line_edit_m.text()))
			elif filtro == "Rubik":
				img = self.rubik(self.pil_im_or.copy(), self.num_colors_rubik)
			elif filtro == "Random Dithering":
				img = self.r_dithering(self.pil_im_or.copy())
			elif filtro == "Fotomosaico":
				img = self.fotomosaico(self.pil_im_or.copy())
			img.show()
			self.pixmap_fil = self.dame_pixmap(img)
			self.label_img_fil.setPixmap(self.pixmap_fil)
			self.label_img_fil.repaint()
		#except Exception:
		#	print("Error en algún parámetro.")


	def dame_img_PIL(self, path):
		img = QImage(path)
		buffer = QBuffer()
		buffer.open(QBuffer.ReadWrite)
		img.save(buffer, Path(path).suffix[1:])
		return Image.open(io.BytesIO(buffer.data()))

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
				n_r = rojo(pixels[i,j]) + cte  
				n_v = verde(pixels[i,j]) + cte
				n_a = azul(pixels[i,j]) + cte
				pixels[i,j] = (255 if (n_r >= 255) else (0 if (n_r <= 0) else n_r), 
				255 if (n_v > 255) else (0 if (n_v < 0) else n_v), 
				255 if (n_a > 255) else (0 if (n_a < 0) else n_a))
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

	def ecualizar_img(self, img):
		gris = self.tono_gris1(img)
		cdf = self.dame_cdf(gris)
		n = gris.size[0]
		m = gris.size[1]
		print(cdf)
		pixels = gris.load()
		nm = n*m
		cdf_min_k = min(cdf.keys(), key=(lambda k: cdf[k]))
		cdf_min = cdf[cdf_min_k]
		nm_cdf_min = nm - cdf_min
		for i in range(n):
			for j in range(m):
				r = rojo(pixels[i,j])
				nuevo_pix = int( ((cdf[str(r)]-cdf_min)/nm_cdf_min) * 255)
				pixels[i,j] = (nuevo_pix, nuevo_pix, nuevo_pix)

		return gris

	def dame_cdf(self, img):
		pixels = img.load()
		cdf = dict()
		val = []
		n = img.size[0]
		m = img.size[1]
		for i in range(n):
			for j in range(m):
				key = str(rojo(pixels[i, j]))
				if cdf == {}:
					c_v = cuenta_val(int(key), pixels, n, m)
					cdf.update([(key, c_v)])
					val += [c_v]
				elif key not in cdf:
					value_prev = val[-1]
					value_this = cuenta_val(int(key), pixels, n, m)
					value_new = value_this + value_prev
					cdf.update([(key, value_new)])
					val += [value_new]
		return cdf

	def semitonosA(self, img, n, m):
		gris = self.tono_gris1(img)
		mosaico = self.mosaico(gris, n, m)
		pixels = mosaico.load()
		
		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		a = []
		size = n, m
		for i in range(1, 11):
			semitono = self.dame_img_PIL("semitonos/a"+ str(i)+ ".jpg")
			semitono.thumbnail(size, Image.ANTIALIAS)
			a.append(semitono)

		for i in range(0, mosaico.size[0],n):
			for j in range(0, mosaico.size[1],m):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 25):
					nueva_img.paste(a[0], (i,j))
				elif (prom >= 25 and prom < 50): 
					nueva_img.paste(a[1], (i,j))
				elif (prom >= 50 and prom < 75): 
					nueva_img.paste(a[2], (i,j))
				elif (prom >= 75 and prom < 100): 
					nueva_img.paste(a[3], (i,j))
				elif (prom >= 100 and prom < 125): 
					nueva_img.paste(a[4], (i,j))
				elif (prom >= 125 and prom < 150): 
					nueva_img.paste(a[5], (i,j))
				elif (prom >= 150 and prom < 175): 
					nueva_img.paste(a[6], (i,j))
				elif (prom >= 175 and prom < 200): 
					nueva_img.paste(a[7], (i,j))
				elif (prom >= 200 and prom < 225): 
					nueva_img.paste(a[8], (i,j))
				elif (prom >= 225 and prom < 255): 
					nueva_img.paste(a[9], (i,j))

		return nueva_img

	def semitonosB(self, img, n, m):
		gris = self.tono_gris1(img)
		mosaico = self.mosaico(gris, n, m)
		pixels = mosaico.load()
		
		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		b = []
		size = n, m
		for i in range(10):
			semitono = self.dame_img_PIL("semitonos/b"+ str(i)+ ".jpg")
			semitono.thumbnail(size, Image.ANTIALIAS)
			b.append(semitono)

		for i in range(0, mosaico.size[0], n):
			for j in range(0, mosaico.size[1], m):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 25):
					nueva_img.paste(b[9], (i,j))
				elif (prom >= 25 and prom < 50): 
					nueva_img.paste(b[8], (i,j))
				elif (prom >= 50 and prom < 75): 
					nueva_img.paste(b[7], (i,j))
				elif (prom >= 75 and prom < 100): 
					nueva_img.paste(b[6], (i,j))
				elif (prom >= 100 and prom < 125): 
					nueva_img.paste(b[5], (i,j))
				elif (prom >= 125 and prom < 150): 
					nueva_img.paste(b[4], (i,j))
				elif (prom >= 150 and prom < 175): 
					nueva_img.paste(b[3], (i,j))
				elif (prom >= 175 and prom < 200): 
					nueva_img.paste(b[2], (i,j))
				elif (prom >= 200 and prom < 225): 
					nueva_img.paste(b[1], (i,j))
				elif (prom >= 225 and prom < 255): 
					nueva_img.paste(b[0], (i,j))

		return nueva_img

	def semitonosC(self, img, n, m):
		gris = self.tono_gris1(img)
		mosaico = self.mosaico(gris, n, m)
		pixels = mosaico.load()
		
		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		c = []
		size = n, m
		for i in range(5):
			semitono = self.dame_img_PIL("semitonos/b"+ str(i)+ ".jpg")
			semitono.thumbnail(size, Image.ANTIALIAS)
			c.append(semitono)

		for i in range(0, mosaico.size[0],n):
			for j in range(0, mosaico.size[1],m):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 50):
					nueva_img.paste(c[4], (i,j))
				elif (prom >= 50 and prom < 100):
					nueva_img.paste(c[3], (i,j))
				elif (prom >= 100 and prom < 150):
					nueva_img.paste(c[2], (i,j))
				elif (prom >= 150 and prom < 200): 
					nueva_img.paste(c[1], (i,j))
				elif (prom >= 200 and prom < 255): 
					nueva_img.paste(c[0], (i,j))

		return nueva_img

	def luz_negra(self, img, peso):
		pixels = img.load()
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				l = int(rojo(pixels[i,j]) * 0.3 + verde(pixels[i,j]) * 0.59 + azul(pixels[i,j]) * 0.11)
				nuevo_r = abs(rojo(pixels[i,j]) - l) * peso
				nuevo_v = abs(verde(pixels[i,j]) - l) * peso
				nuevo_a = abs(azul(pixels[i,j]) - l) * peso
				if nuevo_r > 256:
					nuevo_r = 255
				if nuevo_v > 256:
					nuevo_v = 255
				if nuevo_a > 256:
					nuevo_a = 255
				pixels[i,j] = (nuevo_r, nuevo_v, nuevo_a)

		return img

	def at_t(self, img):
		gris = self.tono_gris1(img)
		alto_c = self.alto_contraste(gris)
		n_s = alto_c.size[0]//18
		puntos = []
		pixels = alto_c.load()
		for i in range(alto_c.size[0]):
			for j in range(0, alto_c.size[1]-n_s, n_s):
				black = 0
				for k in range(j, j+n_s):
					if(int(rojo(pixels[i,k]) * 255) == 0):
						black+=1

				puntos = [False for i in range(n_s)]
				n = black//2

				if(black % 2 == 0):
					m = n-1
				else:
					m = n

				for l in range((n_s//2)-n, (n_s//2)+m):
					puntos[l] = True

				for k in range(j, j+n_s):
					if(puntos[k-j]):
						pixels[i, k] = (0, 0, 0)
					else:
						pixels[i, k] = (255, 255, 255)

			pixels[i, j] = (0, 0, 0)

		return alto_c

	def recursiva_c(self, img, n, m):
		img_t = self.mosaico(img, n, m)
		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		size = n, m

		pixels = img_t.load()
		for i in range(0, img_t.size[0], n):
			for j in range(0, img_t.size[1], m):
				c_web = color_websafe_cercano(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
				nueva_img.paste(c_web, (i-n,j-m, i, j))
				
		return nueva_img

	def recursiva_b(self, img, n, m):
		img_gris = self.tono_gris1(img)
		img_t = self.mosaico(img, n, m)
		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		size = n, m
		t_g = []

		for i in range(20):
			img_b = self.brillo(img_gris.copy(), 127-(i*20))
			img_b.thumbnail(size, Image.ANTIALIAS)
			t_g.append(img_b)

		pixels = img_t.load()
		for i in range(0, img_t.size[0], n):
			for j in range(0, img_t.size[1], m):
				prom = ((rojo(pixels[i, j]) + verde(pixels[i, j]) + azul(pixels[i, j]))//3)
				if (prom >= 0 and prom < 20):
					nueva_img.paste(t_g[19], (i,j))
				elif (prom >= 20 and prom < 30):
					nueva_img.paste(t_g[18], (i,j))
				elif (prom >= 30 and prom < 40):
					nueva_img.paste(t_g[17], (i,j))
				elif (prom >= 40 and prom < 50):
					nueva_img.paste(t_g[16], (i,j))
				elif (prom >= 50 and prom < 60):
					nueva_img.paste(t_g[15], (i,j))
				elif (prom >= 60 and prom < 70):
					nueva_img.paste(t_g[14], (i,j))
				elif (prom >= 70 and prom < 80):
					nueva_img.paste(t_g[13], (i,j))
				elif (prom >= 80 and prom < 90):
					nueva_img.paste(t_g[12], (i,j))
				elif (prom >= 90 and prom < 100): 
					nueva_img.paste(t_g[11], (i,j))
				elif (prom >= 100 and prom < 110): 
					nueva_img.paste(t_g[10], (i,j))
				elif (prom >= 110 and prom < 120): 
					nueva_img.paste(t_g[9], (i,j))
				elif (prom >= 120 and prom < 140): 
					nueva_img.paste(t_g[8], (i,j))
				elif (prom >= 140 and prom < 150): 
					nueva_img.paste(t_g[7], (i,j))
				elif (prom >= 150 and prom < 160): 
					nueva_img.paste(t_g[6], (i,j))
				elif (prom >= 160 and prom < 170): 
					nueva_img.paste(t_g[5], (i,j))
				elif (prom >= 170 and prom < 180): 
					nueva_img.paste(t_g[4], (i,j))
				elif (prom >= 180 and prom < 200): 
					nueva_img.paste(t_g[3], (i,j))
				elif (prom >= 200 and prom < 210): 
					nueva_img.paste(t_g[2], (i,j))
				elif (prom >= 210 and prom < 220): 
					nueva_img.paste(t_g[1], (i,j))
				elif (prom >= 220 and prom < 255): 
					nueva_img.paste(t_g[0], (i,j))
				
		return nueva_img	

	def rubik(self, img, n_colors):
		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		pixels = img.load()

		if n_colors == "256 colores":
			for i in range(img.size[0]):
				for j in range(img.size[1]):
					c_web = color_websafe_cercano(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
					nueva_img.paste(c_web, (i-1,j-1,i,j))
		else:
			for i in range(img.size[0]):
				for j in range(img.size[1]):
					c_rub = self.color_rubik(rojo(pixels[i,j]), verde(pixels[i,j]), azul(pixels[i,j]))
					nueva_img.paste(c_rub, (i-1,j-1, i, j))
				
		return nueva_img


	def color_rubik(self, r, g, b):
		dist = []
		for color_r in self.colores_r:
			d = math.sqrt((r-color_r[0])**2 + (g-color_r[1])**2 + (b-color_r[2])**2)
			dist.append(d)
		closest = min(dist)
		ind = dist.index(closest)
		return self.colores_r[ind]


	def r_dithering(self, img):
		pixels = img.load()
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				v = rojo(pixels[i,j])
				r = random.randint(0, 255)
				if r > v:
					pixels[i,j] = (0, 0, 0)
				else:
					pixels[i,j] = (255, 255, 255)
		return img

	def fotomosaico(self, img):
		n = 9
		m = 9
		mosaico = self.mosaico(img, n, m)
		if(self.imgs_paquete == [] and self.colores_paquete == []):
			self.carga_imgs_fotomosaico(n, m)

		nueva_img = Image.new("RGB", (img.size[0], img.size[1]), (255,255,255))
		size = n, m

		pixels = mosaico.load()
		for i in range(0, img.size[0], n):
			for j in range(0, img.size[1], m):
				index = self.min_dist_euclidiana(pixels[i, j])
				nueva_img.paste(self.imgs_paquete[index], (i,j))

		return nueva_img

	def carga_imgs_fotomosaico(self, n, m):
		if(self.path_fotomosaico):
			f = open(self.path_fotomosaico[0], "r")
			size = n, m
			for line in f:
				tokens = line.split("/") # En el archivo de texto los valores RGB y el directorio están
										 # separados por un /, con split nos deja los tokens que queremos.
				self.colores_paquete.append((int(tokens[0]), int(tokens[1]), int(tokens[2])))
				url = une_tokens(tokens[3:]) # Como el url tmb está separado por / los separa con split, acá hacemos 
											# que la url sea correcta.
				img_mos = Image.open(url)
				img_mos.thumbnail(size, Image.ANTIALIAS)
				self.imgs_paquete.append(img_mos)

			f.close()
		else:
			print("SELECCIONE PRIMERO UN TEXTO CON LA INFO DEL PAQUETE DE IMGS")


	def min_dist_euclidiana(self, pix):
		dist = []
		r = pix[0]
		g = pix[1]
		b = pix[2]
		for color in self.colores_paquete:
			d = math.sqrt((r-color[0])**2 + (g-color[1])**2 + (b-color[2])**2)
			dist.append(d)
		closest = min(dist)
		ind = dist.index(closest)
		return ind

def une_tokens(tokens):
	res = ""
	for token in tokens:
		res += token + "/"
	return res[:-2]

def cuenta_val(color, pixels, n, m):
	cuenta = 0
	for i in range(n):
		for j in range(m):
			if(rojo(pixels[i,j]) == color):
				cuenta+=1
	return cuenta

def color_websafe_cercano(r, g, b):
	r = int(round( ( r / 255.0 ) * 5 ) * 51)
	g = int(round( ( g / 255.0 ) * 5 ) * 51)
	b = int(round( ( b / 255.0 ) * 5 ) * 51)
	return (r, g, b)

def micap(col, img):
	color = col[0]
	pixels = img.load() 
	if color == "rojo":
		for i in range(img.size[0]): 
			for j in range(img.size[1]):   
				pixels[i,j] = (rojo(pixels[i,j]), 0, 0)
	elif color == "verde":
		for i in range(img.size[0]):  
			for j in range(img.size[1]):  
				pixels[i,j] = (0, verde(pixels[i,j]), 0) #ponemos el nuevo color.
	else:
		for i in range(img.size[0]):  
			for j in range(img.size[1]):
				pixels[i,j] = (0, 0, azul(pixels[i,j])) 
	return img


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
