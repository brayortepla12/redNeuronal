from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import random

datos = 0
funActivacionCapa=0
entrenamiento=0

funcActivCapa = []

MatricesPesos=[]
numNeuronas = []
VecUmbrales=[]


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
	global entradas,salidas
	entradas = entradasred
	salidas = salidasred

def Limpiar():
	tabla.delete(*tabla.get_children())

def funActUltimacapa():
    funcActivCapa.append(salActivacion.get())
    global entrenamiento
    entrenamiento = algoEntrenamiento.get()
    messagebox.showinfo(message="Capa salida configurada", title="Configuracion")

def matrizAleatoria(filas,columnas):
    lista2 = []
    for i in range(0,filas):
        lista2.append([])
        for j in range(0,columnas):
            lista2[i].append(round(random.uniform(-1, 1),2))
    return lista2

def vectUmbrales(filas):
    lista2 = []
    for i in range(0,filas):
        lista2.append(round(random.uniform(-1, 1),2))
    return lista2

def mostrarMatriz(matriz,filas,columnas,item):
    root = Tk()
    root.title('Matriz de pesos: '+str(item+1))
    Label(root, text= 'Matriz de pesos: '+str(item+1)).grid(row=0,column=0)
    for r in range(0, filas):
        for c in range(0, columnas):
            cell = Entry(root, width=10)
            cell.grid(row=r+1, column=c)
            cell.insert(0,str(matriz[r][c]).format(r, c))


def genGridMatrizAleatoria():
    #generar matrices python
    for i in range(0,len(numNeuronas)-1):
        MatricesPesos.append(matrizAleatoria(numNeuronas[i],numNeuronas[i+1]))
    #generar vectumbrales python
    for i in range(1,len(numNeuronas)):
        VecUmbrales.append(vectUmbrales(numNeuronas[i]))

    for item in range(len(numNeuronas)-1):
        mostrarMatriz(MatricesPesos[item],int(numNeuronas[item]),int(numNeuronas[item+1]),item)



def confCapasOculta():
    numNeuronas.append(int(labelNumEntradasRed['text']))
    def guaConfCapas():
        numNeuronas.append(int(EntrynumNeuronas.get()))
        funcActivCapa.append(funActivacionCapa)
        EntrynumNeuronas.delete(0,'end')
        messagebox.showinfo(message="Capa configuradas", title="Configuracion")
        if len(numNeuronas) == (int(numCapas.get())+1):
            numNeuronas.append(int(labelNumSalidasRed['text']))
            EntrynumNeuronas['state'] = DISABLED
            messagebox.showinfo(message="Capas ocultas configuradas", title="Configuracion de capas")

    def guaFuncActivacion():
        labelValue = Label(pantallaCapa, textvariable=opcionActivacion)
        global funActivacionCapa
        if int(labelValue['text']) == 1:
            funActivacionCapa = 1
        elif int(labelValue['text']) == 2:
            funActivacionCapa = 2
        elif int(labelValue['text']) == 3:
            funActivacionCapa = 3


    dataNumNeuronas=StringVar()
    pantallaCapa= Tk()
    pantallaCapa.geometry('300x300')
    pantallaCapa.title("Capa oculta")
    textt=StringVar()
    textt.set("CONFIGURAR CAPA")
    Label(pantallaCapa,text=textt.get()).place(x=80,y=20)
    Label(pantallaCapa,text ="Numero de neuronas ").place(x=10,y=80)
    EntrynumNeuronas=Entry(pantallaCapa,width=10,textvariable=dataNumNeuronas)
    EntrynumNeuronas.place(x=140,y=80,width=130,height=20)

    Label(pantallaCapa,text ="Funcion De Activacion").place(x=10,y=130)
    opcionActivacion = IntVar() # Como StrinVar pero en entero

    sigmoide=Radiobutton(pantallaCapa, text="Sigmoide", variable=opcionActivacion,command=guaFuncActivacion, value=1)
    sigmoide.place(x=20,y=160)
    gausiana=Radiobutton(pantallaCapa, text="Gausiana", variable=opcionActivacion,command=guaFuncActivacion, value=2)
    gausiana.place(x=20,y=180)
    tangHiper=Radiobutton(pantallaCapa, text="Tangente Hiperbolica", variable=opcionActivacion,command=guaFuncActivacion, value=3)
    tangHiper.place(x=20,y=200)

    bt=Button(pantallaCapa, text= 'Guardar',command=guaConfCapas).place(width=100,height=30,x=40,y=240)
    Button(pantallaCapa, text= 'Salir').place(width=100,height=30,x=160,y=240)

def pesosTeclado():
    ventana= Tk()
    ventana.geometry('300x300')
    ventana.title("Pesos por teclado")
    ventana.mainloop()

raiz = Tk()
raiz.geometry('800x500')
raiz.resizable(width=False,height=False)
raiz.configure(bg = 'beige')
raiz.title('Aplicación')
tkLabelTitulo = Label(raiz, text=" Rede Neuronal Multicapa ")
tkLabelTitulo.pack()
listapesos=[]

nb = ttk.Notebook(raiz)
nb.pack(expand = 1, fill ="both",padx=50)

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

p2=ttk.Frame(nb)

label_frame1 = LabelFrame(p2, text="Capas ocultas de la red")
label_frame1.pack(fill="both")
label_frame1.place(x=30,y=40,height=110,width=280)

dataNumCapas=StringVar()
Label(label_frame1,text ="Numero de capas ").place(x=10,y=20)
numCapas=Entry(label_frame1,width=10,textvariable=dataNumCapas)
numCapas.place(x=120,y=20,width=130,height=20)
Button(label_frame1, text= 'Configurar',command=confCapasOculta).place(width=100,height=30,x=150,y=50)

label_frame = LabelFrame(p2, text="Capa de salida")
label_frame.pack(fill="both")
label_frame.place(x=30,y=170,height=230,width=635)

label_frame2 = LabelFrame(p2, text="Funcion De Activacion")
label_frame2.pack(fill="both")
label_frame2.place(x=60,y=210,height=130,width=280)

salActivacion = IntVar()
algoEntrenamiento = IntVar()

salsigmoide=Radiobutton(label_frame2, text="Sigmoide", variable=salActivacion, value=1)
salsigmoide.place(x=20,y=10)
salgausiana=Radiobutton(label_frame2, text="Gausiana", variable=salActivacion, value=2)
salgausiana.place(x=20,y=30)
saltangHiper=Radiobutton(label_frame2, text="Tangente Hiperbolica", variable=salActivacion, value=3)
saltangHiper.place(x=20,y=50)
sallineal=Radiobutton(label_frame2, text="Lineal", variable=salActivacion, value=4)
sallineal.place(x=20,y=70)

label_frame3 = LabelFrame(p2, text="Algoritmo entrenamiento")
label_frame3.pack(fill="both")
label_frame3.place(x=360,y=210,height=130,width=280)
regldelta=Radiobutton(label_frame3, text="Regla delta", variable=algoEntrenamiento, value=1)
regldelta.place(x=20,y=10)
regldeltaModificada=Radiobutton(label_frame3, text="Regla delta modificada", variable=algoEntrenamiento, value=2)
regldeltaModificada.place(x=20,y=30)

buttong=Button(label_frame, text= 'Guardar',command=funActUltimacapa).place(width=100,height=30,x=505,y=170)

label_frame4 = LabelFrame(p2, text="Generar Pesos Y umbrales")
label_frame4.pack(fill="both")
label_frame4.place(x=320,y=40,height=110,width=345)

botonAleatorio = Button(label_frame4, text= 'Aleatorio', command=genGridMatrizAleatoria).place(width=100,height=40,x=10,y=20)
botonAteclado = Button(label_frame4, text= 'Por teclado',command=pesosTeclado).place(width=100,height=40,x=120,y=20)
botonSubirPesos = Button(label_frame4, text= 'Subir Pesos').place(width=100,height=40,x=230,y=20)


nb.add(p2,text='Configurar')

raiz.mainloop()