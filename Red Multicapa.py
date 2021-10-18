from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

datos = 0
numNeuronas = []
funcActivCapa = []

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


def confCapasOculta():

    def guaConfCapas():
        numNeuronas.append(EntrynumNeuronas.get())
        print(opcionActivacion.get())
        #aca va el retorno del radio Button

    dataNumNeuronas=StringVar()
    pantallaCapa= Tk()
    pantallaCapa.geometry('300x300')
    pantallaCapa.title("Capa oculta numero ")
    Label(pantallaCapa,text ="CONFIGURAR CAPAS ").place(x=80,y=20)
    Label(pantallaCapa,text ="Numero de neuronas ").place(x=10,y=80)
    EntrynumNeuronas=Entry(pantallaCapa,width=10,textvariable=dataNumNeuronas)
    EntrynumNeuronas.place(x=140,y=80,width=130,height=20)

    Label(pantallaCapa,text ="Funcion De Activacion").place(x=10,y=130)
    opcionActivacion = IntVar() # Como StrinVar pero en entero

    sigmoide=Radiobutton(pantallaCapa, text="Sigmoide", variable=opcionActivacion, value=1)
    sigmoide.place(x=20,y=160)
    gausiana=Radiobutton(pantallaCapa, text="Gausiana", variable=opcionActivacion, value=2)
    gausiana.place(x=20,y=180)
    tangHiper=Radiobutton(pantallaCapa, text="Tangente Hiperbolica", variable=opcionActivacion, value=3)
    tangHiper.place(x=20,y=200)

    Button(pantallaCapa, text= 'Guardar',command=guaConfCapas).place(width=100,height=30,x=100,y=240)

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
label_frame = LabelFrame(p2, text="Capas ocultas de la red")
label_frame.pack(fill="both")
label_frame.place(x=10,y=40,height=110,width=280)

dataNumCapas=StringVar()
Label(label_frame,text ="Numero de capas ").place(x=10,y=20)
numCapas=Entry(label_frame,width=10,textvariable=dataNumCapas)
numCapas.place(x=120,y=20,width=130,height=20)
Button(label_frame, text= 'Guardar',command=confCapasOculta).place(width=100,height=30,x=150,y=50)

nb.add(p2,text='Configurar')

raiz.mainloop()