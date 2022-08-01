




#a = [2932.92, 3146.36, 1068.25, 1048.08, 452.89]
#b = [2002.18, 2002.352, 2002.496, 2001.936, 2002.508]
#print("analise")

#from main import atingiu_setpoint_primeira_vez
temp_funcao = []
temp_energia=[]
temp_tempo=[]
tendencia_anterior="constante"
esta_ligado=False
atingiu_pico_primeira_vez=0
contador_mudar_tendencia=0
tendencia_atual=""
tendencia_anterior=""
medias_minimo=[]
medias_maximo=[]
medias_periodo=[]
medias_potencias=[]
indices=[]
ocorreu_teste=False
texto_usuario=[]
texto_usuario2=[]
medias_minimo_depois=[]
medias_maximo_depois=[]
medias_periodo_depois=[]
medias_potencias_depois=[]
texto_usuario_depois=[]
texto_usuario2_depois=[]
imprimir_energia=""
texto_usuario2=[]
texto_usuario2_depois=[]
z=[0,0,0]
zant=[0,0,0]
ja_colocou_amostra = False
temp_potencia=[]






def tendencia(lista):  #se os ultimos cinco valores estivrem subindo, a tendencia é de subida
	if len(lista)>5:
		if ( lista[-1]>=lista[-2] and lista[-2]>=lista[-3] and lista[-3]>=lista[-4] and lista[-4]>=lista[-5] and lista[-1]!=0 and lista[-2]!=0 ):   
			return "subida"
		elif ( lista[-1]<=lista[-2] and lista[-2]<=lista[-3] and lista[-3]<=lista[-4] and lista[-4]<=lista[-5] and lista[-1]!=0 and lista[-2]!=0 ):
			return "descida"
		else: 
			return "constante"

def colocou_amostra():
	global ja_colocou_amostra
	if ja_colocou_amostra == False: ja_colocou_amostra=True
	else: ja_colocou_amostra=False
	return (ja_colocou_amostra)


def extrair_valores(medias_temperatura, intervalo_energia, intervalo_tempo):
	global medias_minimo
	global medias_maximo
	global medias_periodo
	global medias_potencias
	global indices
	global ocorreu_teste
	global medias_minimo_depois
	global medias_maximo_depois
	global medias_periodo_depois
	global medias_potencias_depois
	global imprimir_energia
	global texto_usuario2
	global texto_usuario2_depois

	
	

	if (len(medias_minimo)>0):
		if (  min(medias_temperatura) < min(medias_minimo) - 8 and sum(indices)==0 ): ocorreu_teste=True; #para ocorrer o teste tem que cair mais que 8 graus
		else: ocorreu_teste=False

		############
	if ( ocorreu_teste and ja_colocou_amostra):
		indices.append(1)	
		energia_consumida_amostra_antes = intervalo_energia - (medias_potencias[len(medias_potencias)-1] *intervalo_tempo)
		print ("ENERGIA CONSUMIDA AMOSTRA")
		print(energia_consumida_amostra_antes)
		imprimir_energia = "Energia total:" + str(intervalo_energia) + "\n" + "Tempo:" + str(intervalo_tempo) + "\n" + "Energia consumida com média antes:" + str(energia_consumida_amostra_antes) + "\n"
		print(imprimir_energia)
		#RETORNAR IMPRIMIR ENERGIA			
		#janela['medias_estudo'].update(imprimir_energia)
		
	#está na média antes do teste
	elif (sum(indices)==0):	
			
		indices.append(0)
		medias_minimo.append(min(medias_temperatura))
		medias_maximo.append(max(medias_temperatura))
		medias_periodo.append((intervalo_tempo)/1000)
		medias_potencias.append(intervalo_energia/intervalo_tempo)

		texto_usuario.append( "potência média:" + str(medias_potencias[(len(medias_potencias)-1)]) + "W min:" + str(min(medias_temperatura)) + "ºC max:" + str(max(medias_temperatura)) + "ºC período:" + str(medias_periodo[(len(medias_potencias)-1)]) + "s \n"       )
		texto_usuario2 = ""
		for i in range(len(texto_usuario)):
			texto_usuario2 = texto_usuario2 + texto_usuario[i]
		print(texto_usuario2)	
		#return (texto_usuario2)   #RETORNAR ISSO PARA IMPRIMIR TELA
		#janela['medias'].update(texto_usuario2)

	#está na média depois do teste
	elif (sum(indices)>0):	
		indices.append(2)
		medias_minimo_depois.append(min(medias_temperatura))
		medias_maximo_depois.append(max(medias_temperatura))
		medias_periodo_depois.append((intervalo_tempo)/1000)
		medias_potencias_depois.append(intervalo_energia/intervalo_tempo)

		texto_usuario_depois.append( "potência média:" + str(medias_potencias_depois[(len(medias_potencias_depois)-1)]) + "W min:" + str(min(medias_temperatura)) + "ºC max:" + str(max(medias_temperatura)) + "ºC período:" + str(medias_periodo_depois[(len(medias_potencias_depois)-1)]) + "s \n"       )
		texto_usuario2_depois = ""
		for i in range(len(texto_usuario_depois)):
			texto_usuario2_depois = texto_usuario2_depois + texto_usuario_depois[i]
		print (texto_usuario2_depois)
		#return (texto_usuario2)   #RETORNAR ISSO PARA IMPRIMIR TELA
		#janela['medias'].update(texto_usuario2)


		##########
	saida = [ texto_usuario2, imprimir_energia, texto_usuario2_depois  ]
	return(saida)	

def reiniciar():
	temp_funcao.clear()
	temp_energia.clear()
	temp_tempo.clear()
	tendencia_anterior="constante"
	esta_ligado=False
	atingiu_pico_primeira_vez=0
	contador_mudar_tendencia=0
	tendencia_atual=""
	tendencia_anterior=""
	medias_minimo.clear()
	medias_maximo.clear()
	medias_periodo.clear()
	medias_potencias.clear()
	indices.clear()
	ocorreu_teste=False
	texto_usuario.clear()
	texto_usuario2.clear()
	medias_minimo_depois.clear()
	medias_maximo_depois.clear()
	medias_periodo_depois.clear()
	medias_potencias_depois.clear()
	texto_usuario_depois.clear()
	texto_usuario2_depois.clear()
	imprimir_energia=""
	texto_usuario2.clear()
	texto_usuario2_depois.clear()
	z=[0,0,0]
	zant=[0,0,0]


def media_15(potencia_atual, esta_ligado):
	calcula_media_movel=[]
	
	if (esta_ligado):
		temp_potencia.append(float(potencia_atual))
		
	if len(temp_potencia)>15:
		for numero in range(-15, 0):
			calcula_media_movel.append( temp_potencia[numero]    )
		#print(calcula_media_movel)
		media_movel=sum(calcula_media_movel)/len(calcula_media_movel)
		calcula_media_movel.clear()	
		return (media_movel)
	else:
		return "x"	

def analisar(temperatura_atual, Energia_colocada, Tempo_conversao):
	global temp_funcao
	global temp_energia
	global temp_tempo
	global atingiu_pico_primeira_vez
	global tendencia_atual
	global tendencia_anterior
	global contador_mudar_tendencia
	global z

	
		
	temp_funcao.append(float(temperatura_atual))
	temp_energia.append(float(Energia_colocada)) 
	temp_tempo.append(float(Tempo_conversao))
	tendencia_momento = tendencia(temp_funcao) 

	#a cada 5 leituras de mudanca de status, udan contador anterior
	#if (contador_mudar_tendencia<0):

	#inicializa a tendencia
	if atingiu_pico_primeira_vez==0 :
		
		if tendencia_momento=="subida": 
			contador_mudar_tendencia+=1
			if contador_mudar_tendencia==4:
				tendencia_atual="subida"
				contador_mudar_tendencia=0
		
		#if tendencia_momento=="descida":  
		#	contador_mudar_tendencia-=1
		#if contador_mudar_tendencia==4: 
		#	tendencia_atual="subida"
		#	tendencia_anterior="descida"
			#atingiu_pico_primeira_vez=1
		#	contador_mudar_tendencia=0

		if tendencia_momento == "descida" and tendencia_atual=="subida": 
			if contador_mudar_tendencia==4:
				tendencia_atual = "descida"
				tendencia_anterior="subida"
				contador_mudar_tendencia=0
		

				print("PRIMEIRO PICO, zerando valores antes")
				atingiu_pico_primeira_vez=1
				#zerar valores antes do pico
				pico = max(temp_funcao)
				for i in range (len(temp_funcao)):
					if (pico == temp_funcao[i]): #i é o índice do pico
						indice_remocao=i
						break
				while (indice_remocao>=0):
					temp_funcao.pop(indice_remocao)
					temp_energia.pop(indice_remocao)
					temp_tempo.pop(indice_remocao)
					indice_remocao-=1
				#temp_funcao=temp_funcao[indice_remocao+1:]

			contador_mudar_tendencia+=1


	else:
		if tendencia_momento == "subida" and tendencia_atual=="descida": 
			if contador_mudar_tendencia==4:
				tendencia_atual="subida"
				tendencia_anterior="descida"
				contador_mudar_tendencia=0
			contador_mudar_tendencia+=1
		
		if tendencia_momento == "descida" and tendencia_atual=="subida": 
			if contador_mudar_tendencia==4:
				tendencia_atual = "descida"
				tendencia_anterior="subida"
				contador_mudar_tendencia=0
				#aqui ocorreu um pico
				print ("TEVE PICO. Fazer análise")
				#achar o pico
				
				
				metade_comparar = int ( (  (len(temp_funcao)) /2 )     )
				pico = max(temp_funcao[metade_comparar:] )  #tira a metade inicial da analise para achar maximo
				
				for i in range (len(temp_funcao)):
					if (pico == temp_funcao[i]): #i é o índice do pico
						indice_remocao=i
						break
				#temp_funcao=temp_funcao[indice_remocao+1:]
				
				intervalo_para_ser_analisado=temp_funcao[:indice_remocao+1]
				intervalo_energia=sum(temp_energia[:indice_remocao+1])
				intervalo_tempo=sum(temp_tempo[:indice_remocao+1])

			
				while (indice_remocao>=0):
					temp_funcao.pop(indice_remocao)
					temp_energia.pop(indice_remocao)
					temp_tempo.pop(indice_remocao)
					indice_remocao-=1

				print("Intervalo a ser analisado:")
				print(intervalo_para_ser_analisado)
				print(intervalo_energia)
				print(intervalo_tempo)
				z = extrair_valores(intervalo_para_ser_analisado, intervalo_energia, intervalo_tempo)

				print("resto")
				print(temp_funcao)
				intervalo_para_ser_analisado.clear()
				





			contador_mudar_tendencia+= 1

	print(temp_funcao)
	print("tendencia atual")
	print(tendencia_atual)
	return(z)

	#if (tendencia(temp_funcao)== and tendencia_anterior==-1 and  atingiu_pico_primeira_vez==0 )


	#if(float(temperatura_atual)>=float(setpoint) and esta_ligado and atingiu_setpoint_primeira_vez==0):	
	#		atingiu_setpoint_primeira_vez=1



	#a cada 3 leituras iguais de tendencia muda tendencia
	#if (tendencia_subida==False)


	#tendencia_subida(temp_funcao)
	
	#esta_ligado=True

#acha se tem tendencia de subida ou tendencia de descida e tendencia superior

#se tendencia de subida and tendencia descida anterior #achou pico
#	se atingiu_setpoint_primeira_vez==0 - achar pico e deletar dele pra frente

#	else achar indice pico e salvar para outra variavel os valores antes ele

'''
a=[113.85, 113.8, 113.69, 113.51, 113.18, 113.09, 112.95, 112.73, 112.47, 112.26, 111.97, 111.73, 111.48, 111.25, 110.97, 110.64, 110.3, 110.09, 109.87, 109.48, 109.25, 108.93, 108.72, 108.4, 108.08, 107.85, 107.51, 107.26, 106.94, 106.57, 106.36, 106.06, 105.84, 105.5, 105.27, 104.91, 104.71, 104.38, 104.09, 103.75, 103.59, 103.27, 103.04, 102.65, 102.45, 102.22, 101.92, 101.63, 101.37, 101.07, 100.88, 100.65, 100.38, 100.04, 99.8, 99.66, 99.26, 99.12, 98.82, 98.57, 98.31, 98.05, 97.85, 97.62, 97.45, 97.23, 97.05, 96.84, 96.81, 96.72, 96.64, 96.54, 96.57, 96.66, 96.73, 96.8, 97.05, 97.3, 97.59, 97.99, 98.41, 98.89, 99.44, 99.96, 100.63, 101.3, 102.09, 102.77, 103.45, 104.19, 105.16, 105.81, 106.7, 107.53, 108.11, 108.93, 109.57, 110.18, 110.76, 111.23, 111.69, 112.1, 112.4, 112.61, 112.88, 112.98, 113.2, 113.34, 113.39]
b = [63.85, 6.8, 13.69, 13.51, 13.18, 13.09, 12.95, 12.73, 12.47, 12.26]
extrair_valores(a, 10555, 100)
extrair_valores(a, 103555, 3100)
extrair_valores(a, 1055, 100)
extrair_valores(b, 1076555, 100)
extrair_valores(a, 1055, 100)
z = extrair_valores(a, 103555, 3100)
print("z:")
print(z[0])
print(z[1])
print(z[2])
'''
