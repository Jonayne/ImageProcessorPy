import sys
import io
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QComboBox, QPushButton, QSlider, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QBuffer, Qt
from PIL import Image
from PIL.ImageQt import ImageQt

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

		self.button_aplicar = QPushButton('Aplicar Tono de gris 1', self)
		self.button_aplicar.setToolTip('Aplique el filtro que escogió.')
		self.button_aplicar.move(230,690)

		self.filtro_escogido = "Tono de gris 1" #El que está por default.

		self.button_aplicar.clicked.connect(self.aplica_filtro)

		self.combo = QComboBox(self)

		# Lista de filtros.
		self.combo.addItem("Tono de gris 1")
		self.combo.addItem("Tono de gris 2")
		self.combo.addItem("Tono de gris 3")
		self.combo.addItem("Tono de gris 4")
		self.combo.addItem("Tono de gris 5")
		self.combo.addItem("Tono de gris 6")
		self.combo.addItem("Tono de gris 7")
		self.combo.addItem("Tono de gris 8")
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
			img.save(buffer, "PNG")
			self.pil_im_or = Image.open(io.BytesIO(buffer.data())) 
			self.label_img_fil.setPixmap(QPixmap())
		except Exception:
			print("Error de lectura de archivo.")
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
		elif text == "Mosaico":
			self.lbl_mos.show()
			self.line_edit_n.show()
			self.line_edit_m.show()
			self.slider.close()
			self.lbl_bri.close()			
		else:
			self.slider.close()
			self.lbl_bri.close()
			self.lbl_mos.close()
			self.line_edit_n.close()
			self.line_edit_m.close()

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

		self.label_img_fil.setPixmap(self.dame_pixmap(img))
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
