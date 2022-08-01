#busca portas seriais
import serial.tools.list_ports as p 
import serial
#from main import *

def busca_serial():
	ports = p.comports()
	port = []
	for i in ports:
		port.append(i.device)
	#print(port)
	return (port)


def inicia_serial(porta):
	try:
		serialArduino = serial.Serial(porta, 115200)

		if serialArduino.isOpen():
			print("Abriu Porta Serial")
		else: print("Erro")
		return(serialArduino)
	except:
		print("Erro")
		return("Erro")

def fecha_serial(x):
	try:
		x.close()
		global serialArduino
		serialArduino = ""
		if x.isOpen():
			print("Porta Serial Aberta")
		else: print("Porta Serial Fechada")

	except:
		print("Porta ja fechada")