#bibliotecas grafica, pyserial, 

from grafico import *	#importa o arquivo com dados da tela
from portaserial import *

import time
#import matplotlib.pyplot as plt    #pip install matplotlib==3.0.0 --user
#import pyqtgraph as pg #biblioteca pyqtgraph para os graficos
#from PyQt5 import QtWidgets, QtCore

#colado

#from pyqtgraph import PlotWidget, plot
#import sys  # We need sys so that we can pass argv to QApplication
#import os
#from random import randint
#import os
#import shutil


nome = ""
portaserial = ""
temperatura = 0
porta_aberta = 0
captura = 0
tempo_total_milisegundos = 0.0
saida_manual=False

#para plotar os graficos
#plt.ion() #habilita modo interativo matplotlib
valores_temperatura=list()
valores_tempo=list()
grafico_temperatura=False
colocou_amostra = False
colocou_amostra_texto = "não"
leitura_recebida = 0
Kp=0
Ki=0
Kd=0
atingiu_setpoint_primeira_vez=0
#soma_para_media_energia=0
#soma_para_media_tempo=0
finalizou_período_negativo=0
temperatura_atual=0
Energia_colocada=0
Tempo_conversao=0
#esta_ligado=False
valores_para_analise=[]
tempo_para_analise=[]
contador_variacao_erro=0
medias_potencias=[]
medias_maximo=[]
medias_minimo=[]
medias_periodo=[]
medias_temperatura=[]
texto_usuario=""
texto_usuario=[]
indices=[]


medias_minimo_depois=[]
medias_maximo_depois=[]
medias_periodo_depois=[]
medias_potencias_depois=[]
texto_usuario_depois=[]
ocorreu_teste=False
z=[0,0,0]
zant=[0,0,0]
astrom=False
Limite_saida=False
MAXIMO_SAIDA_PWM=125
#temp_funcao=[]
from analise import *

#colado
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        #self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        #self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.





#while True:
# #Extrai dados da tela
while True:
				

	#print (nome)
	event, values = janela.Read(timeout=10)
	
	if event == 'Buscar porta' :
		portas = busca_serial()
		print('Portas disponíveis:')
		print(portas)
		janela['selecao'].update(values=portas)
		

	if event == 'selecao' :		#alguma porta serial é selecionada
		portaserial = values['selecao']
		print(portaserial)
		janela['portaserial'].update(portaserial) 
	
	if event == 'Conectar':
		if (porta_aberta==0):  #não aberta
			serialArduino = inicia_serial(portaserial)
			if (serialArduino != "Erro"):
				janela['status'].update('conectado')
				porta_aberta=1

	if event == 'Desconectar':
		try:
			fecha_serial(serialArduino)
			janela['status'].update('desconectado')
			porta_aberta=0
		except:
			print("sem porta aberta")
	
	if event == 'Selecionar':
		temperatura = values['temperatura']
		if temperatura != "":
			tempstring = temperatura + " ºC"
			janela['mostratemperatura'].update(tempstring)
		else: print("Insira a temperatura do teste")

	if event == sg.WIN_CLOSED:  #se fechar a tela interrompe o algoritmo
		texto_str = 'T0\n'
		if (serialArduino.isOpen()):
			serialArduino.write(str.encode(texto_str))
			time.sleep(1)
			serialArduino.write(str.encode(texto_str))
			time.sleep(1)
			fecha_serial(serialArduino) 
			 
		break

	if event == 'Aquecer':

		if porta_aberta == 0:
			print("Verifique conexão")
			janela['ligar'].update('DESLIGADO. Verifique conexão serial')
		elif temperatura==0:
			print("Selecione a temperatura")
			janela['ligar'].update('DESLIGADO. Selecione temperatura')
		elif (float(tensao_atual)<1.0 and int(temperatura)!=0 ):
			print ("Ligue a fonte")
			janela['ligar'].update('DESLIGADO. Ligue a fonte')
		elif (porta_aberta != 0 and int(temperatura)!=0):
			print('Aquecimento ligado para %s graus' %temperatura)
			texto_str = 'T' + str(temperatura) + '\n'
			print(texto_str)
			serialArduino.write(str.encode(texto_str))
			janela['ligar'].update('LIGADO')
			esta_ligado=True

		

		else: print("Verificar a conexão serial")	
    	
	

	if event == 'Desligar':
		if (porta_aberta != 0):
			print('Aquecimento desligado')
			texto_str = 'T0\n'
			print(texto_str)
			serialArduino.write(str.encode(texto_str))
			janela['ligar'].update('DESLIGADO                  ')
			esta_ligado=False

		else: print("verificar conexão")

	if event == 'Definir':
		if (porta_aberta != 0):
			saida_manual_valor = values['saida_manual']
			try: 
				saida_manual_valor_float = float(saida_manual_valor)
				if saida_manual_valor_float >= 0 and saida_manual_valor_float <= 1:
					janela['valor_saida_manual2'].update(saida_manual_valor_float)
					saida_manual_valor_float2 = saida_manual_valor_float

					
				else: print("fora valor")	
			except:
				print("Erro valor")

	if event == 'Ligar Manual':
		if (porta_aberta != 0):
			try:
				saida_string_manual = 'M'+ str(int(saida_manual_valor_float2*MAXIMO_SAIDA_PWM)) +'\n'   #SAIDA DE 0 A MAXIMO_SAIDA_PWM
				serialArduino.write(str.encode(saida_string_manual))
				saida_manual=True
				print("Saida Manual")
				print (saida_manual_valor)
				texto_para_saida = 'Saída: MANUAL:' + str(saida_manual_valor_float)
				janela['saida_status'].update(texto_para_saida)
				#janela['valor_saida_manual'].update(saida_manual_valor_float)
			except:
				print("selecione valor")


	if event == 'Calibrar':
		if (astrom and porta_aberta != 0):
			astrom = False;
			janela['astrom'].update('NÃO')
			serialArduino.write(str.encode("Z"))
			esta_ligado=False
		elif(porta_aberta != 0):
			astrom = True;
			janela['astrom'].update('SIM')
			astrom_temperatura = values['astrom_valor']
			astrom_string = 'Z'+ str(astrom_temperatura) +'\n'   
			serialArduino.write(str.encode(astrom_string))
			esta_ligado=True

			

	if event == 'Limite Saida':
		if (Limite_saida and porta_aberta != 0):
			Limite_saida = False;
			janela['limite_saida_texto'].update('NÃO')
			serialArduino.write(str.encode("Y125"))
			
		elif(porta_aberta != 0):
			limite_saida_valor = values['limite_saida']


			Limite_saida = True;
			limite_saida_numerico = int(float(limite_saida_valor)*MAXIMO_SAIDA_PWM)
			if (limite_saida_numerico>=0 and limite_saida_numerico<=MAXIMO_SAIDA_PWM):
				string_saida_limite = "SIM "+ str(limite_saida_valor)
				janela['limite_saida_texto'].update(string_saida_limite)	
				print(limite_saida_numerico)
				serialArduino.write(str.encode('Y'+ str(limite_saida_numerico) +'\n'))
			else:
				janela['limite_saida_texto'].update('Valor inválido')
			



	if event == 'COLOCOU AMOSTRA':
		ja_colocou_amostra = colocou_amostra()
		if ja_colocou_amostra== True: 
			janela['ja_colocou_amostra'].update('SIM')
		else:
			janela['ja_colocou_amostra'].update('NÃO')
			

	if event == 'Desligar Manual':
		if (porta_aberta != 0):
			janela['saida_status'].update('Saída: AUTOMÁTICA')
			serialArduino.write(str.encode("A"))
			saida_manual=False





	if event == 'Iniciar captura de Dados':
		if not os.path.exists("Resultados"):
			os.makedirs("Resultados")
		
		
		#print( os.getcwd() )
		nome_arquivo = values['arquivo']
		if nome_arquivo != "":
			nome_arquivo=nome_arquivo + ".txt"
			print(nome_arquivo)
			try: 
				#nome_arquivo_pasta = os.path.join("C:/Users/gabri/OneDrive/Área de Trabalho/Calorimetro 2022/Software_python_v2/Resultados", nome_arquivo)
				nome_arquivo_pasta = os.path.join(os.getcwd(), 'Resultados', nome_arquivo)
				print(nome_arquivo_pasta)
				f= open(nome_arquivo_pasta,"x+")
				#f= open(nome_arquivo,"x+")
				arquivo_string = 'Status: Capturando dados em ' + nome_arquivo
				janela['captura'].update(arquivo_string)
				#f.write("Tempo total (s) ;Temperatura 1 (ºC) ; Temperatura 2 (ºC) ;Tensão (V); Corrente (mA) ;Tempo conversão (mS) ;Potencia atual (mW) ;Energia Intervalo (mJ); Amostra Colocada ;Saida")
				#f.write("Tempo total (s) ;Temperatura 1 (ºC) ; Temperatura 2 (ºC) ; Potencia atual (mW) ; Tempo conversão (mS) ;Energia Intervalo (mJ); Saida ; Amostra Colocada")
				f.write("Tempo total (s) ;Temperatura (ºC) ; Potencia atual (W) ; Saida")
				f.write("\n")

				parametros_impressao = "P:" + str(Plido)  + " I:" + str(Ilido) + " D:" + str(Dlido) + " Tensão:" + str( round(tensao_em_vazio,4) ) + " V " + "Temperatura ambiente: " + str(temperatura_atual2) + "ºC"  "\n" 
				f.write(parametros_impressao)

				
				captura = 1
				tempo_total_milisegundos=0;
				#f.close() 
			except:
				print("Nome já Existe. Escolha outro")
				janela['captura'].update('Status: Já existe o nome do arquivo. Escolha outro')

		else: 
			print('Insira nome para salvar os dados')
			janela['captura'].update('Status: Inserir nome para salvar os dados')

	if event == 'Parar captura de Dados':
		try:
			f.close()
			janela['captura'].update('Status: Captura terminada')
			captura=0

		except:
			print("Não fechou o arquivo ou captura não iniciada")

	if event == 'Colocou amostra':
		if (colocou_amostra):
			colocou_amostra = False;
			janela['colocou_amostra'].update('NÃO')
			colocou_amostra_texto = "não"
		else:
			colocou_amostra = True;
			janela['colocou_amostra'].update('SIM')
			colocou_amostra_texto = "sim"


	
	if event == 'Configurar':	
		Kp = values['Kp']
		Ki = values['Ki']
		Kd = values['Kd']
		Kpf=float(Kp)*1000
		Kif=float(Ki)*1000
		Kdf=float(Kd)*1000
		configurar_KPKIKD = 'P'+ str(Kpf) +'\n'   
		serialArduino.write(str.encode(configurar_KPKIKD))
		time.sleep(1)
		configurar_KPKIKD = 'I'+ str(Kif) +'\n'   
		serialArduino.write(str.encode(configurar_KPKIKD))
		time.sleep(1)
		configurar_KPKIKD = 'D'+ str(Kdf) +'\n'   
		serialArduino.write(str.encode(configurar_KPKIKD))
		print(Kpf)
		print(Kif)
		print(Kdf)
		
	if event == 'Salvar':
		print("Salvar")
		serialArduino.write(str.encode("S"))


	if (porta_aberta != 0):
		linhaLida = serialArduino.readline()
		
		try:
			linhaLida = linhaLida.decode('utf-8')
		except:
			print("erro decode\n")	
		print(linhaLida)
		
		if linhaLida[0]=='P':
			Plido= linhaLida[2:9]
			Ilido=linhaLida[11:18]
			Dlido=linhaLida[20:27]
			try: 
				janela['PIDstatus'].update("P="+ Plido + " I=" + Ilido + " D=" + Dlido)

			 
			except: print("erro pegar KP")


		if linhaLida[0]=='L':
			try: temperatura_atual = "{:.2f}".format(float(linhaLida[1:9]))
			except: print("erro conversao temperatura 1")	
			#try: tensao_atual = "{:.3f}".format(float(linhaLida[20:27]))
			#except: print("erro conversao tensao")	
			tensao_atual = linhaLida[20:27]
			try: corrente_atual = "{:.4f}".format(float(linhaLida[40 :47]))
			except: print("erro conversao corrente")	
			#try: Tempo_conversao = "{:.3f}".format(float(linhaLida[71:80]))
			#except: print("erro conversao tempo")
			Tempo_conversao = linhaLida[71:80]
			try: Saida_pwm = "{:.3f}".format(float(linhaLida[93:100])/float(MAXIMO_SAIDA_PWM))
			except: print("erro conversao pwm")	
			try: Saida_pwm2 = linhaLida[93:100]
			except: print("erro conversao pwm 2")

			try: Numero_leitura = int(linhaLida[111:118])
			except: print("erro conversao numero leitura")	
			#try: Energia_colocada = "{:.2f}".format(float(linhaLida[140:149]))
			#except: print("erro conversao energia")
			Energia_colocada = (linhaLida[140:149])

			temperatura_atual2 = linhaLida[166:175]
			

			tempo_total_milisegundos = tempo_total_milisegundos + float(Tempo_conversao)

			#valores_temperatura.append("{:.1f}".format(float(temperatura_atual)))
			#valores_tempo.append("{:.1f}".format(tempo_total_milisegundos/1000))

			tempo_total_segundos = "{:.2f}".format(tempo_total_milisegundos/1000)
			#print(valores_temperatura)
			#print(valores_tempo)

			#calculo de potencia e energia
			#potencia_atual = "{:.2f}".format(float(tensao_atual)*float(corrente_atual))
			potencia_atual = "{:.6f}".format(float(Energia_colocada)/float(Tempo_conversao))
			
			if float(potencia_atual)==0: 
				potencia_atual="00000.00"
				tensao_em_vazio = float(tensao_atual )
			#energia_intervalo = "{:.3f}".format(float(tensao_atual)*float(corrente_atual)*float(Tempo_conversao)/1000)

			janela['temperatura_atual'].update(temperatura_atual)
			janela['temperatura_atual_aba2'].update(temperatura_atual)
			janela['temperatura_atual2'].update(temperatura_atual2)
			janela['tensao_atual'].update(tensao_atual)
			corrente_atual=str(  round( float(corrente_atual)    ,2)      )
			janela['corrente_atual'].update(corrente_atual)
			janela['Tempo_conversao'].update(Tempo_conversao)
			janela['Saida_pwm'].update(Saida_pwm)
			janela['Numero_leitura'].update(Numero_leitura)
			potencia_atual_impressao=str(  round( float(potencia_atual)    ,4)      )
			janela['potencia_atual'].update(potencia_atual_impressao)
			#janela['energia'].update(Energia_colocada)

			potencia_movel = media_15(float(potencia_atual), esta_ligado)
			try:
				potencia_movel = round(float(potencia_movel),4)
			except: print()
			janela['potencia_movel'].update(str(potencia_movel))

			if (Numero_leitura==1):
				leitura_recebida = 0
			leitura_recebida = leitura_recebida+1
			janela['leitura_recebida'].update(leitura_recebida)
			#if (grafico_temperatura):
			#	plt.plot(valores_tempo, valores_temperatura)
			#	plt.show(block=False)

			if captura==1:
				#texto_salvar = tempo_total_segundos + " ; " + temperatura_atual + " ; " +temperatura_atual2  + " ; " + tensao_atual + " ; " +corrente_atual+ " ; " + Tempo_conversao + " ; " + potencia_atual + " ; " + Energia_colocada+ " ; " + colocou_amostra_texto+ " ; " + Saida_pwm + "\n"
				#texto_salvar = tempo_total_segundos + " ; " + temperatura_atual + " ; " +temperatura_atual2  + " ;   " + potencia_atual + " ; " +  Tempo_conversao + " ; " + Energia_colocada+ " ; " + Saida_pwm2 + " ; " + colocou_amostra_texto + "\n"
				texto_salvar = tempo_total_segundos + " ; " + temperatura_atual + " ;   " + potencia_atual + " ; " +   Saida_pwm2 + "\n"
				texto_salvar = texto_salvar.replace(".",",")   #troca de ponto para virgula
				f.write(texto_salvar)
		'''		
			############Analise dos dados pelos picos
			
			z = analisar(temperatura_atual, Energia_colocada, Tempo_conversao)
			#print(z)
			#print(zant)
			if(z[0]!=zant[0]): janela['medias2'].update(z[0])  #antes
			if(z[1]!=zant[1]): janela['medias_estudo2'].update(z[1])  #teste
			if(z[2]!=zant[2]): janela['medias_depois2'].update(z[2])	#depois
			zant[0]=z[0]
			zant[1]=z[1]
			zant[2]=z[2]
			
			#print (temp_funcao)
			
			#################analise dos dados pelos picos
		'''

		#y = media_50(potencia_atual, esta_ligado)

		# Análise dos resultados
		#começa quando atingiu setpoint pela primeira vez		
		

		#AQUI
		if(astrom and float(temperatura_atual)>=float(astrom_temperatura) and esta_ligado and atingiu_setpoint_primeira_vez==0):	
			atingiu_setpoint_primeira_vez=1

		#elimina a primeira meia curva positiva
		if (astrom and atingiu_setpoint_primeira_vez==1 and float(temperatura_atual)<=float(astrom_temperatura) ):
			atingiu_setpoint_primeira_vez=2
				

		#começa a análise somando a parte inferior da onda	
		if(astrom and float(temperatura_atual)<=float(astrom_temperatura) and atingiu_setpoint_primeira_vez==2 and esta_ligado):	#MEIO CICLO POSITIVO
			

			#até atingir temperatura mínima, verifica se é hora propícia de colocar amostra
			'''revisao
			if( (len(medias_minimo)>0)):
				if (float(temperatura_atual)-medida_anterior<0):
					janela['pode_colocar_amostra'].update('SIM')
				else: janela['pode_colocar_amostra'].update('NÃO')
			'''


			medida_anterior = float(temperatura_atual)  #para detectar o periodo descrescente do periodo negativo
				
			#quando acaba o ciclo de análise
			if (finalizou_período_negativo==1): 
								
				#medias_potencias.append(sum(valores_para_analise)/sum(tempo_para_analise))
				#medias_maximo.append(max(medias_temperatura))
				
				#detecta quando ocorre o teste (temperatura cai 10 graus a menos que a mínima das mínimas)
				'''revisao
				if (len(medias_minimo)>0):
					if (  min(medias_temperatura) < min(medias_minimo) - 10 and sum(indices)==0 ): ocorreu_teste=True; #para ocorrer o teste tem que cair mais que 10 graus
					else: ocorreu_teste=False
				'''
				#medias_minimo.append(min(medias_temperatura))
				#medias_periodo.append(sum(tempo_para_analise)/1000)

				#na variavel indices, guarda 0 se for antes do teste; 1 se for o teste e 2 se for depois do teste
				#se ocorreu antes do teste, vai salvar na tela correspondente do software
				
				'''revisao
				#considera sendo o teste se teve pelo menos 3 testes e caiu 5 graus a menos que o minimo
				if ( ocorreu_teste ):
					indices.append(1)
					energia_do_teste=sum(valores_para_analise)
					tempo_do_teste = sum(tempo_para_analise)			
					energia_consumida_amostra_antes = energia_do_teste - (medias_potencias[len(medias_potencias)-1] *tempo_do_teste)
					#energia_consumida_amostra_depois
					print ("ENERGIA CONSUMIDA AMOSTRA")
					print(energia_consumida_amostra_antes)
					imprimir_energia = "Energia total:" + str(energia_do_teste) + "\n" + "Tempo:" + str(tempo_do_teste) + "\n" + "Energia consumida com média antes:" + str(energia_consumida_amostra_antes) + "\n"
					
					janela['medias_estudo'].update(imprimir_energia)
				'''
				'''revisao-estava dentro if
				#está na média antes do teste
				elif (sum(indices)==0):	
				'''	
				#indices.append(0)
				medias_minimo.append(min(medias_temperatura))
				medias_maximo.append(max(medias_temperatura))
				medias_periodo.append(sum(tempo_para_analise)/1000)
				medias_potencias.append(sum(valores_para_analise)/sum(tempo_para_analise))
				#texto_usuario.append( "potência média:" + str(medias_potencias[(len(medias_potencias)-1)]) + "W min:" + str(medias_minimo[(len(medias_potencias)-1)]) + "ºC max:" + str(medias_maximo[(len(medias_potencias)-1)]) + "ºC período:" + str(medias_periodo[(len(medias_potencias)-1)]) + "s \n"       )
				variacao_temperatura = round (max(medias_temperatura) - min(medias_temperatura),2)
				imprimir_periodo = round(medias_periodo[(len(medias_potencias)-1)], 2)
				P_calibrado = round((159.15/variacao_temperatura)*0.6,2)
				I_calibrado = round(0.5*imprimir_periodo,2)
				D_calibrado = round(0.125*imprimir_periodo,2)

				texto_usuario.append( "potência média:" + str(  round(medias_potencias[(len(medias_potencias)-1)],3)  ) + "W min:" + str(min(medias_temperatura)) + "ºC max:" + str(max(medias_temperatura)) +  "ºC  variação:" + str(variacao_temperatura )       + "ºC período:" + str(imprimir_periodo) + "s P:" + str(P_calibrado) + " I:" + str(I_calibrado) + " D:" + str(D_calibrado) +   "\n"       )
				texto_usuario2 = ""
				for i in range(len(texto_usuario)):
					texto_usuario2 = texto_usuario2 + texto_usuario[i]
				janela['medias'].update(texto_usuario2)

				#está na média depois do teste
				
				'''revisao
				elif (sum(indices)>0):	
					indices.append(2)
					medias_minimo_depois.append(min(medias_temperatura))
					medias_maximo_depois.append(max(medias_temperatura))
					medias_periodo_depois.append(sum(tempo_para_analise)/1000)
					medias_potencias_depois.append(sum(valores_para_analise)/sum(tempo_para_analise))
					#texto_usuario_depois.append( "potência média:" + str(medias_potencias_depois[(len(medias_potencias_depois)-1)]) + "W min:" + str(medias_minimo_depois[(len(medias_potencias_depois)-1)]) + "ºC max:" + str(medias_maximo_depois[(len(medias_potencias_depois)-1)]) + "ºC período:" + str(medias_periodo_depois[(len(medias_potencias_depois)-1)]) + "s \n"       )
					texto_usuario_depois.append( "potência média:" + str(medias_potencias_depois[(len(medias_potencias_depois)-1)]) + "W min:" + str(min(medias_temperatura)) + "ºC max:" + str(max(medias_temperatura)) + "ºC período:" + str(medias_periodo_depois[(len(medias_potencias_depois)-1)]) + "s \n"       )
										#min(medias_temperatura)

					texto_usuario2_depois = ""
					for i in range(len(texto_usuario_depois)):
						texto_usuario2_depois = texto_usuario2_depois + texto_usuario_depois[i]
					janela['medias_depois'].update(texto_usuario2_depois)	
				
				'''
					


				print(medias_potencias)

				#texto_usuario.append( "Período " + str(i) + " potência média:" + str(medias_potencias[i]) + "W min:" + str(medias_minimo[i]) + "ºC max:" + str(medias_maximo[i]) + "ºC período:" + str(medias_periodo[i]) + "s \n"       )
				#texto_usuario.append( "potência média:" + str(medias_potencias[(len(medias_potencias)-1)]) + "W min:" + str(medias_minimo[(len(medias_potencias)-1)]) + "ºC max:" + str(medias_maximo[(len(medias_potencias)-1)]) + "ºC período:" + str(medias_periodo[(len(medias_potencias)-1)]) + "s \n"       )
				#for i in range (0,(len(medias_potencias) )):
				#	texto_usuario= texto_usuario + "Período " + str(i) + " potência média:" + str(medias_potencias[i]) + "W min:" + str(medias_minimo[i]) + "ºC max:" + str(medias_maximo[i]) + "ºC período:" + str(medias_periodo[i]) + "s \n"
				
				

				valores_para_analise.clear()
				tempo_para_analise.clear()
				finalizou_período_negativo=0
				contador_variacao_erro=0
				medias_temperatura.clear() #COLOQUEI AQUI


			#em toda leitura, incrementa os valores 
			valores_para_analise.append( float(Energia_colocada)  )
			tempo_para_analise.append( float(Tempo_conversao)  )
			medias_temperatura.append(float(temperatura_atual))
			#print(valores_para_analise) #COMENTAR AQUI

		#análise do meio ciclo positivo
		if(astrom and float(temperatura_atual)>float(astrom_temperatura) and atingiu_setpoint_primeira_vez==2 and esta_ligado): #MEIO CICLO NEGATIVO. Quando acaba esse, acabou o período e deve calcular média
			#soma_para_media_energia=float(Energia_colocada)+soma_para_media_energia
			#soma_para_media_tempo = float(Tempo_conversao) + soma_para_media_tempo
			if (contador_variacao_erro>2):  #elimina eventual imprecisao quando chega na inversao
				finalizou_período_negativo=1 
			contador_variacao_erro = contador_variacao_erro +1
			valores_para_analise.append( float(Energia_colocada)  )
			tempo_para_analise.append( float(Tempo_conversao)  )
			medias_temperatura.append(float(temperatura_atual))

			
			#print(valores_para_analise) #COMENTAR AQUI
			#print(tempo_para_analise) 

	

	if event == 'Reiniciar':
		'''
		reiniciar()
		z=[0,0,0]
		zant=[0,0,0]
		janela['medias2'].update(z[0])  #antes
		janela['medias_estudo2'].update(z[1])  #teste
		janela['medias_depois2'].update(z[2])	#depois

		'''
		atingiu_setpoint_primeira_vez=0
		medias_minimo.clear()
		medias_temperatura.clear()
		ocorreu_teste=False
		indices.clear()
		medias_minimo.clear()
		medias_maximo.clear()
		medias_periodo.clear()
		medias_potencias.clear()
		texto_usuario.clear()
		medias_minimo_depois.clear()
		medias_maximo_depois.clear()
		medias_periodo_depois.clear()
		medias_potencias_depois.clear()
		texto_usuario_depois.clear()
		valores_para_analise.clear()
		tempo_para_analise.clear()
		finalizou_período_negativo=0
		contador_variacao_erro=0
		#janela['medias_depois'].update('')
		janela['medias'].update('')
		#janela['medias_estudo'].update('')
		

	if event == 'Grafico temperatura':
		#if (grafico_temperatura==True):
		#	grafico_temperatura=False
		#else: grafico_temperatura=True
	#	plt.plot(valores_tempo, valores_temperatura)
	#	plt.show(block=False)
		#pw = pg.plot(valores_tempo, valores_temperatura, pen='r')  # plot x vs y in red
		#pw.plot(valores_tempo, valores_temperatura, pen='b')
		#x = np.random.normal(size=1000)
		#y = np.random.normal(size=1000)
		#pg.plot(valores_tempo, valores_temperatura, pen=None, symbol='o') 
		#pg.plot(valores_tempo, valores_temperatura, pen=None, symbol='o') 
		app = QtWidgets.QApplication(sys.argv)
		w = MainWindow()
		w.show()
		sys.exit(app.exec_())
		
		