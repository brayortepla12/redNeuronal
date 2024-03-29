from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import math
import random
import pickle
import matplotlib.pyplot as plt

datos = 0
funActivacionCapa=0
entrenamiento=0

funcActivCapa = []

MatricesPesos=[]
numNeuronas = []
VecUmbrales=[]

rataAprendizaje=0
errMaxPermitido=0
numIteraciones=0

def reinicializarRed():
    global MatricesPesos,rataAprendizaje,errMaxPermitido,numIteraciones,VecUmbrales,funActivacionCapa,funcActivCapa,entrenamiento,numNeuronas
    numNeuronas=[]
    entrenamiento=0
    funActivacionCapa=0
    funcActivCapa=[]
    MatricesPesos=[]
    VecUmbrales=[]
    rataAprendizaje=0
    errMaxPermitido=0
    numIteraciones=0

    entryrataAprendizaje.delete(0,'end')
    entryerrMaxPermitido.delete(0,'end')
    entrynumIteraciones.delete(0,'end')

def abrir_archivo():
    archivo = filedialog.askopenfilename(initialdir ='/',title='Selecione archivo',filetype=(('xlsx files', '*.xlsx*'),('All files', '*.*')))
    indica['text'] = archivo
    return archivo

def abrir_archivo2():
    archivo = filedialog.askopenfilename(initialdir ='/',title='Selecione archivo',filetype=(('xlsx files', '*.xlsx*'),('All files', '*.*')))
    indica2['text'] = archivo
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

def datos_excel2():
    datos_obtenidos = indica2['text']
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
    tabla2['column'] = list(df.columns)
    tabla2['show'] = "headings"  #encabezado

    for columna in tabla2['column']:
        tabla2.heading(columna, text= columna)
        tabla2.column(columna,width=115,anchor=CENTER)
    df_fila = df.to_numpy().tolist()

    for fila in df_fila:
        tabla2.insert('', 'end', values =fila)

def subir_pesos():
    messagebox.showinfo(message="Pesos cargados Correctamente", title="Pesos Sinapticos")

    with open("pesosOptimos.pkl", "rb") as f:
        pesosCargados=(pickle.load(f))

    with open("Umbrales.pkl", "rb") as f:
        umbalesCargados=(pickle.load(f))

    print(pesosCargados)
    print('***********')
    print(umbalesCargados)

    global MatricesPesos,VecUmbrales
    MatricesPesos=pesosCargados
    VecUmbrales=umbalesCargados

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
    elem=0
    lista2 = []
    for i in range(0,filas):
        lista2.append([])
        for j in range(0,1):
            lista2[i].append(round(random.uniform(-1, 1),2))
            elem=elem+1
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
        MatricesPesos.append(matrizAleatoria(numNeuronas[i+1],numNeuronas[i]))
    #generar vectumbrales python
    for i in range(1,len(numNeuronas)):
        VecUmbrales.append(vectUmbrales(numNeuronas[i]))

    for item in range(len(numNeuronas)-1):
        mostrarMatriz(MatricesPesos[item],int(numNeuronas[item+1]),int(numNeuronas[item]),item)


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
            numCapas.delete(0,'end')


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

p=0
u=0
def pesosTeclado():
    listapesos=[]
    def almacenarPeso():
        global p
        listapesos.append(float(entryp.get()))
        entryp.delete(0,'end')
        if(len(MatricesPesos)!=(len(numNeuronas)-1)):
            if(len(listapesos)>=(numNeuronas[p]*numNeuronas[p+1])):
                messagebox.showinfo(message="Matriz De Peso Guardado", title="Peso Capa")
                gridMostrarPesosTeclado(numNeuronas[p+1],numNeuronas[p])
                p=p+1
        else:
            messagebox.showinfo(message="Todos los pesos fueron cargados", title="Pesos")
            entryp['state'] = DISABLED

    def pesosmatrizTeclado(filas,columnas):
        elem=0
        lista2 = []
        for i in range(0,filas):
            lista2.append([])
            for j in range(0,columnas):
                lista2[i].append(listapesos[elem])
                elem=elem+1
        MatricesPesos.append(lista2)
        return lista2

    def gridMostrarPesosTeclado(filas,columnas):
        lista2 = pesosmatrizTeclado(filas,columnas)
        root = Tk()
        for r in range(0, filas):
            for c in range(0, columnas):
                cell = Entry(root,width=10)
                cell.grid(padx=5, pady=5, row=r, column=c)
                cell.insert(0, str(lista2[r][c]).format(r, c))
        but = ttk.Button(root, text="salir")
        but.grid(column=0,row=r+1,padx=5,pady=10)
        del listapesos[:]

    #umbrales por teclado
    listaumbrales=[]
    def umbrales():
        global u
        listaumbrales.append(float(entryu.get()))
        entryu.delete(0,'end')
        if(len(VecUmbrales)!=(len(numNeuronas)-1)):
            if(len(listaumbrales)>=(numNeuronas[u+1])):
                messagebox.showinfo(message="Umbral guardado", title="Umbrales")
                gridMostrarUmbrlTeclado(numNeuronas[u+1],1)
                u=u+1
        else:
            messagebox.showinfo(message="Todos los umbrales fueron cargados", title="Umbrales")
            entryu['state'] = DISABLED
#error generar umbrales (lista dentro de lista)
    def umbralesTeclado(filas,columnas):
        elem=0
        lista2 = []
        for i in range(0,filas):
            lista2.append([])
            for j in range(0,1):
                lista2[i].append(listaumbrales[elem])
                elem=elem+1
        VecUmbrales.append(lista2)
        return lista2

    def gridMostrarUmbrlTeclado(filas,columnas):
        lista2 = umbralesTeclado(filas,columnas)
        root = Tk()
        for r in range(0, filas):
            for c in range(0, columnas):
                cell = Entry(root,width=10)
                cell.grid(padx=5, pady=5, row=r, column=c)
                cell.insert(0, str(lista2[r][c]).format(r, c))
        but = ttk.Button(root, text="salir")
        but.grid(column=0,row=r+1,padx=5,pady=10)
        del listaumbrales[:]

    root = Tk()
    root.geometry('350x250')
    root.title('Pesos y umbrales')
    frameP = LabelFrame(root, text="Pesos sinapticos")
    frameP.pack(fill="both")
    frameP.place(x=30,y=20,height=100,width=290)

    Label(frameP,text='Ingresar Peso: ').place(x=20,y=10)
    entryp=Entry(frameP,width=10,)
    entryp.place(x=130,y=10,width=130,height=20)
    Button(frameP,text='Guardar',command=almacenarPeso).place(x=170,y=40,width=90,height=30)

    frameU = LabelFrame(root, text="Umbrales")
    frameU.pack(fill="both")
    frameU.place(x=30,y=140,height=100,width=290)

    Label(frameU,text='Ingresar Umbral: ').place(x=20,y=10)
    entryu=Entry(frameU,width=10,)
    entryu.place(x=130,y=10,width=130,height=20)
    Button(frameU,text='Guardar',command=umbrales).place(x=170,y=40,width=90,height=30)

def configuracion():
    ra=float(entryrataAprendizaje.get())
    emp=entryerrMaxPermitido.get()
    ni=entrynumIteraciones.get()

    global rataAprendizaje,errMaxPermitido,numIteraciones
    rataAprendizaje = ra
    errMaxPermitido = emp
    numIteraciones = ni
    messagebox.showinfo(message="Cofiguracion Guardada Correctamente", title="Configuracion")

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

def sigmoid(x):
    z = np.exp(-x)
    sig = 1 / (1 + z)
    return sig

def lineal(z):
    return np.maximum(0, z)

def Neurona(data):#NEURONA
    #peso=MatricesPesos[0]
    #umbral=VecUmbrales[0]
    m=0
    conjuntosSalidas=[]
    l=[]

    for element in data:
        l.append(element)
    conjuntosSalidas.append(l)
    bandFuncAct=0
    for matriz in MatricesPesos:
        listSalidas=[]
        m=m+1
        for i in range(0,len(matriz)):
            s=0
            for j in range(0,len(matriz[0])):
                s=s+((matriz[i][j])*(float(data[j])))
            s=s-VecUmbrales[m-1][i][0]

            if(funcActivCapa[bandFuncAct]==3):
                #salidaNeurona = truncate(math.tanh(s),5)
                salidaNeurona = math.tanh(s)
                #print('tang Hipervolica')
            elif(funcActivCapa[bandFuncAct]==1):
                salidaNeurona = sigmoid(s)
                #print('sigmoide')
            elif(funcActivCapa[bandFuncAct]==2):
                salidaNeurona = math.tanh(s)
                #print('gaussiana')
            elif(funcActivCapa[bandFuncAct]==4):
                salidaNeurona = lineal(s)
                #print('lineal')


            listSalidas.append(salidaNeurona)
        bandFuncAct+=1
        conjuntosSalidas.append(listSalidas)
        data=listSalidas
        #print('list salidas: '+str(listSalidas))
    return conjuntosSalidas

def muticapa(data):
    sumErrores = np.array([])
    filas = data.shape[0]
    columnas = data.shape[1]
    encontrado=False

    for itm in range(0,int(numIteraciones)):
        errorIteracion = []
        errorPatron=0
        for i in range(0,filas):
            errorLineal = []
            entradaActual=data[i,0:columnas-salidas]
            salidaDeseada=data[i,columnas-salidas:]
            salidaObtenida=Neurona(entradaActual)
            sumerrLineal=0

            for elemento in range(0,salidas):
                errorLineal.append(salidaDeseada[elemento] - salidaObtenida[len(salidaObtenida)-1][elemento])
                sumerrLineal=sumerrLineal+abs(errorLineal[elemento])

            errorPatron = sumerrLineal/salidas
            #print('error de patron: '+str(errorPatron))
            errorIteracion.append(errorPatron)
            numMatriz=0

            banderaentradas=0
            for matriz in MatricesPesos:
                numMatriz=numMatriz+1
                #print('Matriz peso anterior: '+str(matriz))
                for i in range(0,len(matriz)):
                    for j in range(0,len(matriz[0])):
                        if(numMatriz == len(MatricesPesos)):
                            #matriz[i][j]=truncate(matriz[i][j]+(rataAprendizaje*errorLineal[i]*salidaObtenida[banderaentradas][j]),3)
                            matriz[i][j]=matriz[i][j]+(rataAprendizaje*errorLineal[i]*salidaObtenida[banderaentradas][j])
                            #print('error lineal: '+str(errorLineal[i]))
                        else:
                            #matriz[i][j]=truncate(matriz[i][j]+(rataAprendizaje*errorPatron*salidaObtenida[banderaentradas][j]),3)
                            matriz[i][j]=matriz[i][j]+(rataAprendizaje*errorPatron*salidaObtenida[banderaentradas][j])
                            '''print('valor matriz: '+str(matriz[i][j]))
                            print('error patron: '+str(errorPatron))
                            print('salida: '+str(salidaObtenida[banderaentradas][j]))'''
                banderaentradas=+1
                #print('Matriz peso actualizada: '+str(matriz))

            #print('*****************************************\n')
            numMatriz=0
            for umbral in VecUmbrales:
                numMatriz=numMatriz+1
                #print('Matriz umbral anterior: '+str(umbral))
                for i in range(0,1):
                    for j in range(0,len(umbral)):
                        if(numMatriz == len(VecUmbrales)):
                            umbral[j][i]=truncate(umbral[j][i]+(rataAprendizaje*errorLineal[j]*1),3)
                            #umbral[j][i]=umbral[j][i]+(rataAprendizaje*errorLineal[j]*1)
                            #print('error lineal: '+str(errorLineal[j]))
                        else:
                            umbral[j][i]=truncate(umbral[j][i]+(rataAprendizaje*errorPatron*1),3)
                            #umbral[j][i]=umbral[j][i]+(rataAprendizaje*errorPatron*1)
                #print('Matriz umbral Actualizado: '+str(umbral))
        '''print('**********')
        print('error iteracion: '+str(sum(errorIteracion)))
        print('num de patrones: '+str(filas))
        print('erms: '+str((sum(errorIteracion)/filas)))'''

        sumErrores = np.append(sumErrores,sum(errorIteracion)/filas)

        if(sum(errorIteracion)/filas<=float(errMaxPermitido)):
            print('red entrenada: '+' el error erms '+str(sum(errorIteracion)/filas)+' es menor o igual a el error maximo permitido '+str(errMaxPermitido))

            with open("pesosOptimos.pkl", "wb") as f:
                pickle.dump(MatricesPesos, f)

            with open("Umbrales.pkl", "wb") as f:
                pickle.dump(VecUmbrales, f)

            with open("FuncActivaciones.pkl", "wb") as f:
                pickle.dump(funcActivCapa, f)
            encontrado=True
            break

    figura = plt.figure()
    plt.title(u'Error por Iteración')
    plt.xlabel('Patrones')
    plt.ylabel(u'Error ERMS')
    plt.plot(range(1,sumErrores.shape[0]+1),sumErrores,'bo-')
    plt.grid(True)
    plt.xticks(range(1,sumErrores.shape[0]+1))
    plt.show()

    if(encontrado!=True):
        resultado = messagebox.askretrycancel("Reintentar","No se entreno\nDesea reinicializar la red ?")
        if resultado == True:
            reinicializarRed()
            print('reiniciar')


def entrenar():
    data=datos.to_numpy()
    muticapa(data)

def simular():
    with open("FuncActivaciones.pkl", "rb") as f:
        obj = pickle.load(f)

    global funcActivCapa
    funcActivCapa = obj
    evalSalidas = []
    data=datos.to_numpy()
    filas = data.shape[0]
    columnas = data.shape[1]
    for i in range(0,filas):
        errorLineal = []
        entradaActual=data[i,0:columnas-salidas]
        salidaDeseada=data[i,columnas-salidas:]
        salidaObtenida=Neurona(entradaActual)

        for elemnto in salidaObtenida[len(salidaObtenida)-1]:
            evalSalidas.append(round(elemnto))

        if set(salidaDeseada) == set(evalSalidas):
            messagebox.showinfo('Informacion', 'Patron Aprendido')
            plt.title(u'salida deseada V/S salida obtenida')
            plt.xlabel('Numero de salidas')
            plt.ylabel(u'Salidas')
            x2 = salidaDeseada
            x3 = evalSalidas
            plt.plot(x2, 'rd', x3, 'g^')
            plt.show()
            print(evalSalidas)
        else:
            messagebox.showerror('Informacion', 'La red no conoce este patron')
            plt.title(u'salida deseada V/S salida obtenida')
            plt.xlabel('Numero de salidas')
            plt.ylabel(u'Salidas')
            x2 = salidaDeseada
            x3 = evalSalidas
            plt.plot(x2, 'rd', x3, 'g^')
            plt.show()
            print(evalSalidas)
            muticapa(data)



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
botonSubirPesos = Button(label_frame4, text= 'Subir Pesos',command=subir_pesos).place(width=100,height=40,x=230,y=20)

nb.add(p2,text='Configurar')

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


nb.add(p3,text='Entrenar')

p4=ttk.Frame(nb)
frame5 = Frame(p4, bg='gray26')
frame5.place(x=50, y=30, width=590, height=180)
frame6 = Frame(p4, bg='gray26')
frame6.place(x=50,y=220,width=590,height=70)

tabla2 = ttk.Treeview(frame5 , height=7)
tabla2.place(x=0, y=0, width=590)

ladox = Scrollbar(frame5, orient = HORIZONTAL, command= tabla.xview)
ladox.place(x=0,y=163,width=575)
ladoy = Scrollbar(frame5, orient =VERTICAL, command = tabla.yview)
ladoy.place(x=573,y=0,height=180)
tabla2.configure(yscrollcommand = ladoy.set,xscrollcommand = ladox.set)

boto1 = Button(frame6, text= 'Abrir',command = abrir_archivo2)
boto1.grid(column = 0, row = 0, sticky='nsew', padx=10, pady=10)
boto1.configure(width=20,height=1)

boto2 = Button(frame6, text= 'Mostrar',command= datos_excel2)
boto2.grid(column = 1, row = 0, sticky='nsew', padx=10, pady=10)
boto2.configure(width=20,height=1)

boto3 = Button(frame6, text= 'Limpiar',command= Limpiar)
boto3.grid(column = 2, row = 0, sticky='nsew', padx=10, pady=10)
boto3.configure(width=20,height=1)

indica2 = Label(frame6, fg= 'white', bg='gray26', text= 'Ubicación Del Archivo', font= ('Arial',8,'bold') )
indica2.place(x=8,y=40)

Button(p4, text= 'Simular patron',command=simular).place(width=100,height=40,x=50,y=310)


nb.add(p4,text='Simular')

raiz.mainloop()