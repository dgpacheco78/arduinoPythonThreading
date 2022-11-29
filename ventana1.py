import tkinter as tk
import serial
import time
import json
import threading

arduino = serial.Serial("COM6", 9600, timeout=1.0)
time.sleep(2)

        
def enviarDato():
    while True:
        global dato0, dato1, dato2
        cad = arduino.readline().decode('ascii').strip()
        print(cad)
        validaJson1 = json_validator(cad)
        if validaJson1 == True:
            htJson = json.loads(cad)
            print("Mensaje dentro de la funcion " , cad)
            hume = htJson["hume"]
            temC = htJson["temC"]
            temF = htJson["temF"]
            dato0.set(hume)
            dato1.set(temC)
            dato2.set(temF)
        time.sleep(1)
        arduino.flushInput()

hilo = threading.Thread(target = enviarDato, daemon = True)
hilo.start()

def escribir():
    print("Prueba")

def close():
    root.destroy()  # Cierra la ventana
    arduino.close() # Cierra la conexion
    hilo.join()

def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json: %s" % error)
        return False

def servoM(v):
    global valor1
    valor1.set(v)
    arduino.write(v.encode('ascii'))
    print("servo " + v)
    v = ""
    #time.sleep(1)

    
root = tk.Tk()
root.wm_protocol('WM_DELETE_WINDOW',close)
root.geometry("450x350")
root.title("Leer")
dato0 = tk.StringVar()
dato1 = tk.StringVar()
dato2 = tk.StringVar()
valor1 = tk.StringVar()

tk.Label(root,text="Lecturas del sensor DHT11", font=('Georgia 20')).place(x=10,y=10)
tk.Label(root,text="Humedad", font=('Georgia 20')).place(x=10,y=60)
tk.Label(root,text="Grados C", font=('Georgia 20')).place(x=10,y=100)
tk.Label(root,text="Grados F", font=('Georgia 20')).place(x=10,y=140)
tk.Entry(root, width=10, textvariable= dato0, justify='center', font=('Georgia 20')).place(x=200,y=60)
tk.Entry(root, width=10, textvariable= dato1, justify='center', font=('Georgia 20')).place(x=200,y=100)
tk.Entry(root, width=10, textvariable= dato2, justify='center', font=('Georgia 20')).place(x=200,y=140)

tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, length=200, command=servoM, font=('Georgia 20')).place(x=10,y=200)
tk.Label(root, bg='white', fg='black', width=20).place(x=10,y=50)
tk.Entry(root, width=8, textvariable= valor1, justify='center', font=('Georgia 20')).place(x=10,y=280)
root.mainloop()