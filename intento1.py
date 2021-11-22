from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np


# Función para registrar al usuario
def registrar_usuario():
    usuario_info = usuario.get() #Obtenemos la información almacenada en usuario
    contra_info = contra.get() #Obtenemos la información almacenada en contra

    archivo = open(usuario_info, "w") #Abrimos la información en modo escritura
    archivo.write(usuario_info + "\n") #Escribimos la infor
    archivo.write(contra_info)
    archivo.close()

    # Limpiamos los text variable
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    #Ahora le diremos al usuario que su ingreso ha sido exitoso
    Label(pantalla1, text="Registro convencional exitoso", fg="green", font=("Calibri", 11)).pack()


# Función para el registro facial
def registro_facial():
    #Capturamos el rostro
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read() #Leemos el video
        cv2.imshow('Registro facial', frame) #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img + ".jpg", frame) #Guardamos la última captura como imagen y le asignamos el nombre del usuario
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END) #Limpiamos los text variable
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro facial exitoso", fg="green", font=("Calibri", 11)).pack()


# Detectamos el rostro y exportamos los pixeles
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2, = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(usuario_img + ".jpg", cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img + ".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)


# Función para asignar al boton registro
def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("300x250") #Asignamos el tamaño de la ventana

    #Creamos las entradas
    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text="Registro facial: debe asignar un usuario: ").pack()
    Label(pantalla1, text="Registro tradicional: debe asignar un usuario y una contraseña: ").pack()
    Label(pantalla1, text="").pack() #Espacio entre campos
    Label(pantalla1, text="Usuario * ").pack() #Mostramos en la pantalla 1 en usuario
    usuario_entrada = Entry(pantalla1, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la información
    usuario_entrada.pack()
    Label(pantalla1, text="Contraseña *").pack() #Mostramos en la papntalla 1 la contraseña
    contra_entrada = Entry(pantalla1, textvariable = contra) #Creamos un text variable para que el usuario ingrese la contraseña
    contra_entrada.pack()
    Label(pantalla1, text="").pack() #Espacio entre campos
    Button(pantalla1, text="Registro tradicional", width=15, height=1, command= registrar_usuario).pack() #Creamos el boton

    #Boton para el registro facial
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro facial", width=15, height=1, command= registro_facial).pack()


# Función para verificar los datos ingresados al login
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(o, END)
    contra_entrada2.delete(o, END)

    lista_archivos = os.listdir()
    if log_usuario in lista_archivos: #Comparamos los archivos con el que nos interesa
        archivo2 = open(log_usuario, "r") #Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines() #Leerá las lineas del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesión exitoso")
            Label(pantalla2, text="Inicio de sesión exitoso", fg="green", font=("Calibri", 11)).pack()
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text="Contraseña incorrecta", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


# Función para el login facial
def login_facial():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('Login facial', frame)
        if cv2.waitKey(1) == 27: #Cuando oprimamos "Esc" se romperá el video
            break
    usuario_login = verificacion_usuario.get() #Con es ta variable vamos aguardar la foto, pero con otro nombre para no sobreescribir
    cv2.imwrite(usuario_login + "LOG.jpg", frame) #Guardamos la última captura como imagen y le asignamos el nombre del usuario
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END) #Limpiamos los text variable
    contra_entrada2.delete(0, END)


    # Función para guardar el rostro
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2, = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(usuario_login + "LOG.jpg", cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    # Detectamos el rostro
    img = usuario_login + "LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)


    # Función para comparar los rostros
    def orb_sim(img1, img2):
        orb = cv2.ORB_create() #Creamos el objeto de comparación

        kpa, descr_a = orb.detectAndCompute(img1, None) #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None) #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos el comparador de fuerza

        matches = comp.match(descr_a, descr_b) #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos clave
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches) #Exportamos el porcentaje de la similitud


    # Importamos las imagenes y llamamos la función de comparación
    im_archivos = os.listdir() #Vamos a importar la lista de archivos con la libreria os
    if usuario_login + ".jpg" in im_archivos: #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread(usuario_login + ".jpg", 0) #Importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login + "LOG.jpg", 0) #Importamos el rostro del inicio de sesión
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.9:
            Label(pantalla2, text="Inicio de sesión exitoso", fg="green", font=("Calibri", 11)).pack()
            print("Bienvenido al sistema: ", usuario_login)
            print("Compatibilidad con la foto del registro: ", similitud)
        else:
            print("Rostro incorrecto, verifique su usuario")
            print("Compatibilidad con la foto del registro: ", similitud)
            Label(pantalla2, text="Incompatibilidad de rostros", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


# Función para asignar al boton login
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x250") #Creamos la ventana
    Label(pantalla2, text="Login facial: debe asignar un usuario").pack()
    Label(pantalla2, text="Login tradicional: debe asignar un usuario y contraseña").pack()
    Label(pantalla2, text="").pack()

    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

    # Ingresamos los datos
    Label(pantalla2, text="Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text="Contraseña *").pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
    contra_entrada2.pack()
    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesión tradicional", width=20, height=1, command= verificacion_login).pack()

    # Creamos el boton para hacer el login facial
    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesión facial", width=20, height=1, command= login_facial).pack()


# Función pantalla principal
def pantalla_principal():
    global pantalla #Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("300x250") #Tamaño de la ventana
    pantalla.title("Login")
    Label(text="Login Inteligente", bg="gray", width="300", height="2", font=("Verdana", 13)).pack()

    # Botones
    Label(text="").pack() #Espacio entre el titulo y el primer boton
    Button(text="Iniciar Sesión", height="2", width="30", command= login).pack()
    Label(text="").pack() #Espacio entre el primer y segundo boton
    Button(text="Registro", height="2", width="30", command= registro).pack()

    pantalla.mainloop()

pantalla_principal()