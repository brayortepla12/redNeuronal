from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

datos = 0
matrizPeso = 0
rataAprendizaje = 0
errMaxPermitido = 0
numIteraciones = 0
entradas = 0
salidas = 0

def abrir_archivo():
	archivo = filedialog.askopenfilename(initialdir ='/',title='Selecione archivo',filetype=(('xlsx files', '*.xlsx*'),('All files', '*.*')))
	indica['text'] = archivo
	return archivo


def datos_excel():
	datos_obtenidos = indica['text']
	try:
		archivoexcel = r'{}'.format(datos_obtenidos)
		df = pd.read_excel(archivoexcel)
		global datos
		datos = df
		mostradatos(df)
	except ValueError:
		messagebox.showerror('Informacion', 'Formato incorrecto')
		return None
	except FileNotFoundError:
		messagebox.showerror('Informacion', 'El archivo esta \n malogrado')
		return None
	Limpiar()
	tabla['column'] = list(df.columns)
	tabla['show'] = "headings"  #encabezado
	for columna in tabla['column']:
		tabla.heading(columna, text= columna)
		tabla.column(columna,width=115,anchor=CENTER)
	df_fila = df.to_numpy().tolist()

	for fila in df_fila:
		tabla.insert('', 'end', values =fila)

#----------------------- VISTA -------------------------------

def almacenarPeso():
	listapesos.append(float(entrada.get()))
	entrada.delete(0,'end')

	if len(listapesos) >= (int(labelNumEntradasRed['text']) * int(labelNumSalidasRed['text'])):
		entrada['state'] = DISABLED
		messagebox.showinfo(message="Pesos Guardadaos Correctamente", title="Pesos Sinapticos")


def subir_pesos():
	messagebox.showinfo(message="Pesos cargados Correctamente", title="Pesos Sinapticos")
	global matrizPeso
	matrizPeso=np.loadtxt('PesosOptimos.txt',dtype=float)



def mostradatos(archivo):
	entradasred=0
	salidasred=0
	for element in archivo.columns:
		if 'x' in element or 'X' in element :
			entradasred=entradasred+1
		else:
			salidasred=salidasred+1
	labelNumEntradasRed['text']=entradasred
	labelNumSalidasRed['text']=salidasred
	labelNumPatronesRed['text']=len(archivo)
	labelNumSalidasDeRedRed['text']=salidasred
	labelNumNeuronasRed['text']=labelNumSalidasDeRedRed['text']
	global entradas,salidas
	entradas = entradasred
	salidas = salidasred


def pesosmatrizTeclado():
	elem=0
	lista2 = []
	for i in range(int(labelNumEntradasRed['text'])):
		lista2.append([])
		for j in range(int(labelNumSalidasRed['text'])):
			lista2[i].append(listapesos[elem])
			elem=elem+1
	global matrizPeso
	matrizPeso = lista2
	return lista2


def gridMostrarPesosTeclado():
	messagebox.showinfo(message="Pesos Generados", title="Pesos Sinapticos")
	lista2 = pesosmatrizTeclado()
	root = Tk()
	for r in range(0, int(labelNumEntradasRed['text'])):
		for c in range(0, int(labelNumSalidasRed['text'])):
			cell = Entry(root,width=10)
			cell.grid(padx=5, pady=5, row=r, column=c)
			cell.insert(0, str(lista2[r][c]).format(r, c))
	but = ttk.Button(root, text="salir")
	but.grid(column=0,row=r+1,padx=5,pady=10)
	root.mainloop()


def pesosmatrizAleatoria():
	lista2 = []
	for i in range(int(labelNumEntradasRed['text'])):
		lista2.append([])
		for j in range(int(labelNumSalidasRed['text'])):
			lista2[i].append(float(random.randint(-1, 1)))
	global matrizPeso
	matrizPeso = lista2
	return lista2


def gridMostrarPesosAleatorio():
	messagebox.showinfo(message="Pesos Generados", title="Pesos Sinapticos")
	lista2=pesosmatrizAleatoria()
	root = Tk()
	for r in range(0, int(labelNumEntradasRed['text'])):
		for c in range(0, int(labelNumSalidasRed['text'])):
			cell = Entry(root,width=10)
			cell.grid(padx=5, pady=5, row=r, column=c)
			cell.insert(0, str(lista2[r][c]).format(r,c))
	but = ttk.Button(root, text="salir")
	but.grid(column=0,row=r+1,padx=5,pady=10)
	root.mainloop()


def configuracion():
	ra=entryrataAprendizaje.get()
	emp=entryerrMaxPermitido.get()
	ni=entrynumIteraciones.get()

	global rataAprendizaje,errMaxPermitido,numIteraciones
	rataAprendizaje = ra
	errMaxPermitido = emp
	numIteraciones = ni
	messagebox.showinfo(message="Cofiguracion Guardada Correctamente", title="Configuracion")


def Limpiar():
	tabla.delete(*tabla.get_children())

#----------------------- LOGICA -------------------------------

raiz = Tk()
raiz.geometry('800x500')
raiz.resizable(width=False,height=False)
raiz.configure(bg = 'beige')
raiz.title('Aplicación')
tkLabelTitulo = Label(raiz, text=" Redes Neuronales ")
tkLabelTitulo.pack()
listapesos=[]

nb = ttk.Notebook(raiz)
nb.pack(expand = 1, fill ="both",padx=50)

#------------------------carga datos--------------------------

def funRampa(x):# funcion rampa
    if (x < 0):
        resultado = 0
    elif (x >= 0 and x <= 1):
        resultado = -1 #quiere decir que la salida sera igual a la entrada
    elif (x>1):
        resultado = 1
    return resultado

def funEscalon(x):# funcion escalon
    if(x>0):
        resultado = 1
    elif (x<=0):
        resultado = 0
    return resultado

def Neurona(data,pesos):#NEURONA
	soma=[]
	for i in range(0,salidas):
		s=0
		for j in range(0,entradas):
			s=s+(data[j]*pesos[j][i])
		if opcionActivacion==1:
			soma = 'sin programar'
		else:
			soma.append(funEscalon(s))
	return(soma)


def algoDel_PeceptonSimple(data):
	sumErrores = np.array([])
	filas = data.shape[0]
	columnas = data.shape[1]
	for itm in range(0,int(numIteraciones)):
		errorIteracion = []
		errorPatron=0
		for i in range(0,filas):
			errorLineal = []
			entradaActual=data[i,0:columnas-salidas]
			salidaDeseada=data[i,columnas-salidas:]
			salidaObtenida=Neurona(entradaActual,matrizPeso)
			print('entrada actual: '+str(entradaActual))
			print('salida deseada: '+str(salidaDeseada))
			print('salida optenida: '+str(salidaObtenida))

			for salobt in range(0,salidas):
				errorLineal.append(abs(salidaDeseada[salobt] - salidaObtenida[salobt]))
			print('error lineal: '+str(errorLineal))
			errorPatron = sum(errorLineal)/salidas
			errorIteracion.append(errorPatron)

			for i in range(0,salidas):
				for j in range(0,entradas):
					print('peso anterior: '+str(matrizPeso[j][i]))
					matrizPeso[j][i] = matrizPeso[j][i]+(float(rataAprendizaje)*float(errorLineal[i])*entradaActual[j])
					print('peso final: '+str(matrizPeso[j][i]))
		print('error iteracion: '+ str(errorIteracion))
		print('********************************')
		sumErrores = np.append(sumErrores,sum(errorIteracion)/filas)

		if(sum(errorIteracion)/filas<=float(errMaxPermitido)):
			np.savetxt('PesosOptimos.txt', matrizPeso,'%.4f')
			break

	figura = plt.figure()
	plt.title(u'Error por Iteración')
	plt.xlabel('Patrones')
	plt.ylabel(u'Error Lineal')
	plt.plot(range(1,sumErrores.shape[0]+1),sumErrores,'bo-')
	plt.grid(True)
	plt.xticks(range(1,sumErrores.shape[0]+1))
	plt.show()

def entrenar():
	data=datos.to_numpy()
	algoDel_PeceptonSimple(data)


p1=ttk.Frame(nb)
nb.add(p1,text='Cargar')

labelNumEntradas = Label(p1,text ="Numero De Entradas: ").place(x=50,y=40)
labelNumEntradasRed = Label(p1,text ="")
labelNumEntradasRed.place(x=170,y=40)

labelNumSalidas = Label(p1,text ="Numero De Salidas: ").place(x=50,y=80)
labelNumSalidasRed = Label(p1,text ="")
labelNumSalidasRed.place(x=170,y=80)

labelNumPatrones = Label(p1,text ="Numero De Patrones: ").place(x=250,y=40)
labelNumPatronesRed = Label(p1,text ="")
labelNumPatronesRed.place(x=380,y=40)

labelNumSalidasDeRed = Label(p1,text ="Numero De Ralidas Red: ").place(x=250,y=80)
labelNumSalidasDeRedRed = Label(p1,text =" ")
labelNumSalidasDeRedRed.place(x=380,y=80)

labelNumNeuronas = Label(p1,text ="Numero De Neuronas: ").place(x=470,y=40)
labelNumNeuronasRed = Label(p1,text =" ")
labelNumNeuronasRed.place(x=600,y=40)

frame1 = Frame(p1, bg='gray26')
frame1.place(x=50, y=130, width=590, height=180)
frame2 = Frame(p1, bg='gray26')
frame2.place(x=50,y=330,width=590,height=70)

tabla = ttk.Treeview(frame1 , height=7)
tabla.place(x=0, y=0, width=590)

ladox = Scrollbar(frame1, orient = HORIZONTAL, command= tabla.xview)
ladox.place(x=0,y=163,width=575)
ladoy = Scrollbar(frame1, orient =VERTICAL, command = tabla.yview)
ladoy.place(x=573,y=0,height=180)
tabla.configure(yscrollcommand = ladoy.set,xscrollcommand = ladox.set)

boton1 = Button(frame2, text= 'Abrir',command = abrir_archivo)
boton1.grid(column = 0, row = 0, sticky='nsew', padx=10, pady=10)
boton1.configure(width=20,height=1)

boton2 = Button(frame2, text= 'Mostrar',command= datos_excel)
boton2.grid(column = 1, row = 0, sticky='nsew', padx=10, pady=10)
boton2.configure(width=20,height=1)

boton3 = Button(frame2, text= 'Limpiar',command= Limpiar)
boton3.grid(column = 2, row = 0, sticky='nsew', padx=10, pady=10)
boton3.configure(width=20,height=1)

indica = Label(frame2, fg= 'white', bg='gray26', text= 'Ubicación Del Archivo', font= ('Arial',8,'bold') )
indica.place(x=8,y=40)

#------------------------Configuracion--------------------------

p2=ttk.Frame(nb)
labelFunActivacion = Label(p2,text ="Funcion De Activacion").place(x=50,y=40)
opcionActivacion = IntVar() # Como StrinVar pero en entero

radioRampa=Radiobutton(p2, text="Rampa", variable=opcionActivacion, value=1)
radioRampa.pack()
radioRampa.place(x=50,y=70)
radioEscalon=Radiobutton(p2, text="Escalon", variable=opcionActivacion,value=2)
radioEscalon.pack()
radioEscalon.place(x=50,y=100)

labelAlgEntrenamiento = Label(p2,text ="Algoritmo De Entrenamoento").place(x=50,y=140)
opcionAlgoritmo = IntVar() # Como StrinVar pero en entero

radioDelta=Radiobutton(p2, text="Regla Delta", variable=opcionAlgoritmo, value=1)
radioDelta.pack()
radioDelta.place(x=50,y=170)

label_frame = LabelFrame(p2, text="Generar Pesos Sinapticos")
label_frame.pack(fill="both")
label_frame.place(x=230,y=40,height=100,width=430)

botonAleatorio = Button(label_frame, text= 'Aleatorio',command=gridMostrarPesosAleatorio).place(width=120,height=40,x=10,y=20)
botonAteclado = Button(label_frame, text= 'Por teclado',command=gridMostrarPesosTeclado).place(width=120,height=40,x=150,y=20)
botonSubirPesos = Button(label_frame, text= 'Subir Pesos',command=subir_pesos).place(width=120,height=40,x=290,y=20)
framePesTeclado = LabelFrame(p2, text="Dijitar Pesos")

framePesTeclado.pack(fill="both")
framePesTeclado.place(x=320,y=160,height=100,width=290)

dato=StringVar()
Label(framePesTeclado,text ="Ingresa Peso: ").place(x=20,y=10)
entrada=Entry(framePesTeclado,width=10,textvariable=dato)
entrada.place(x=140,y=10,width=130,height=20)
Button(framePesTeclado, text= 'Guardar',command=almacenarPeso).place(width=100,height=30,x=170,y=40)

p3=ttk.Frame(nb)

label_frame2 = LabelFrame(p3)
label_frame2.pack(fill="both")
label_frame2.place(x=30,y=30,height=190,width=340)

rataAprendizaje = StringVar()
errMaxPermitido = StringVar()
numIteraciones = StringVar()

Label(p3,text ="Rata De Aprendizaje : ").place(x=50,y=40)
entryrataAprendizaje=Entry(p3,width=10,textvariable=rataAprendizaje)
entryrataAprendizaje.place(x=210,y=40,width=130,height=20)

Label(p3,text ="Erorr Maximo Permitido : ").place(x=50,y=80)
entryerrMaxPermitido=Entry(p3,width=10,textvariable=errMaxPermitido)
entryerrMaxPermitido.place(x=210,y=80,width=130,height=20)

Label(p3,text ="Numero De Iteraciones : ").place(x=50,y=120)
entrynumIteraciones=Entry(p3,width=10,textvariable=numIteraciones)
entrynumIteraciones.place(x=210,y=120,width=130,height=20)

Button(p3, text= 'Guardar',command=configuracion).place(width=180,height=40,x=100,y=165)
Button(p3, text= 'Entrenar',command=entrenar).place(width=180,height=40,x=440,y=95)
p4=ttk.Frame(nb)

nb.add(p2,text='Configurar')
nb.add(p3,text='Entrenar')
nb.add(p4,text='Simular')

raiz.mainloop()

