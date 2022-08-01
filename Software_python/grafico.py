#Usa a bibliotecas PySimpleGUI; pySerial


import PySimpleGUI as sg 

portas = []

sg.theme('dark grey 4')




#layout
layout1 = [
	[sg.Text('Conexão serial',size=(20, 1), font='Lucida',justification='left'), sg.Text('Status:'), sg.Text('desconectado', key='status')],
	[sg.Button('Buscar porta'), sg.Combo(portas, size=(10, 1), enable_events=True, key='selecao'), sg.Text('Porta selecionada:'), sg.Text('nenhuma',size=(7, 1), key=('portaserial')), sg.Button('Conectar'),sg.Button('Desconectar')],
	[sg.Text('')],
	[sg.Text('Dados',size=(20, 1), font='Lucida',justification='left')],
	
	[sg.Text('Temperatura Atual:'), sg.Text('0', key='temperatura_atual'),sg.Text('ºC     ')   , sg.Text('Temperatura ambiente:'), sg.Text('0', key='temperatura_atual2'),sg.Text('ºC')         ],
	#[sg.Text('Temperatura:'), sg.Text('0', key='temperatura_atual'),sg.Text('ºC     ')      ],
	[sg.Text('Tensao:'), sg.Text('0', key='tensao_atual'), sg.Text('V                       '), sg.Text('Corrente:'), sg.Text('0', key='corrente_atual'), sg.Text('mA')      ],     
	[sg.Text('Tempo de conversão:'), sg.Text('0', key='Tempo_conversao'),sg.Text('mS      '), sg.Text('Saída pwm'), sg.Text('0', key='Saida_pwm'), sg.Text('     '), sg.Text('Leitura:'), sg.Text('0', key='Numero_leitura'), sg.Text(' / ') , sg.Text('0', key='leitura_recebida')           ],
	#[sg.Text('Potência:'), sg.Text('0', key='potencia_atual'), sg.Text('W               '), sg.Text('Energia:'), sg.Text('0', key='energia'), sg.Text('mJ')       ],
	[sg.Text('Potência:'), sg.Text('0', key='potencia_atual'), sg.Text('W               '), sg.Text('Média móvel potência (15):'), sg.Text('x', key='potencia_movel'), sg.Text('W               '),         ],
	#[sg.Button('Colocou amostra'), sg.Text('NÃO', key='colocou_amostra')		],
	#[sg.Text('Pode colocar amostra:'), sg.Text('NÃO', key='pode_colocar_amostra')  ],
	#[sg.Text('Setup de corrente'), sg.Input(size=(10,0),key=('corrente'))],
	[sg.Text('')],
	[sg.Text('Saida manual',size=(20, 1), font='Lucida',justification='left'), sg.Text('Saída: AUTOMÁTICA', key='saida_status')   ],
	[sg.Text('Saída manual (entre 0 e 1):'), sg.Text('   ', key='valor_saida_manual2'), sg.Input(size=(10,0),key=('saida_manual')),  sg.Button('Definir'), sg.Button('Ligar Manual'), sg.Button('Desligar Manual')  ],
	[sg.Text('')],
	[sg.Text('PID',size=(20, 1), font='Lucida',justification='left')],
	[sg.Text('PID '), sg.Input('0', size=(10,0),key=('Kp')), sg.Input('0',size=(10,0),key=('Ki')), sg.Input('0', size=(10,0),key=('Kd')), sg.Button('Configurar'), sg.Text('KP= KI = KD= ', key='PIDstatus')     ],
	#[sg.Input('0', size=(10,0),key=('astrom_valor')), sg.Button('ASTROM'), sg.Text('NÃO', key='astrom')],
	[sg.Text('')],
	[sg.Text('Ensaio',size=(20, 1), font='Lucida',justification='left')],
	[sg.Text('Temperatura do ensaio:'), sg.Text('não selecionado', size=(12, 1), key='mostratemperatura'),  sg.Input(size=(10,0),key=('temperatura')), sg.Button('Selecionar')],
	[sg.Text('Comandos:'), sg.Button('Aquecer'), sg.Button('Desligar'), sg.Text('DESLIGADO', key='ligar')],
	#[sg.Input('1', size=(10,0),key=('limite_saida')), sg.Button('Limite Saida'), sg.Text('NÃO', key='limite_saida_texto')],

	[sg.Text('')],
	[sg.Text('Captura de Dados',size=(20, 1), font='Lucida',justification='left'), sg.Text('Status: captura não iniciada', key='captura') ],
	[sg.Text('Nome do arquivo'), sg.Input(size=(14,0),key=('arquivo')),sg.Button('Iniciar captura de Dados'), sg.Button('Parar captura de Dados')],
	#[sg.Button('Grafico temperatura')]
	#[sg.Output(size=(70,8), key='-OUTPUT-')]

]

#layout
layout2 = [
	[sg.Text('Calibração PID',size=(20, 1), font='Lucida',justification='left')],
	[sg.Text('Temperatura Atual:'), sg.Text('0', key='temperatura_atual_aba2'),sg.Text('ºC     ') ],
	[sg.Input('0', size=(10,0),key=('astrom_valor')), sg.Button('Calibrar'), sg.Text('NÃO', key='astrom')],
	#[sg.Text('Pode colocar amostra:'), sg.Text('NÃO', key='pode_colocar_amostra')  ],
	[sg.Text('Calibração usando método de Astrom e Hagglund e calibração final por Ziegler-Nichols (por frequência) ')],
	[sg.Text('Colocar temperatura do teste e clicar em Calibrar')],
	[sg.Multiline('',size=(100,15), key=('medias') )],
	#[sg.Text('Quando médias é maior que 3 e detecta que a temperatura caiu mais de 10ºC da mínima do ciclo, inicia teste')],
	#[sg.Multiline('Teste',size=(90,5), key=('medias_estudo') )],
	#[sg.Multiline('Medias depois',size=(90,5), key=('medias_depois') )],
	[sg.Button('Reiniciar')],

	]


#layout picos
layout3 = [
	[sg.Text('Análise',size=(20, 1), font='Lucida',justification='left')],
	#[sg.Text('Temperatura Atual:'), sg.Text('0', key='temperatura_atual_aba2'),sg.Text('ºC     ') ],
	#[sg.Text('Pode colocar amostra:'), sg.Text('NÃO', key='pode_colocar_amostra')  ],
	#[sg.Text('Somente com PID oscilante')],
	[sg.Multiline('Médias por período:',size=(90,10), key=('medias2') )],
	#[sg.Text('Quando médias é maior que 3 e detecta que a temperatura caiu mais de 10ºC da mínima do ciclo, inicia teste')],
	[sg.Multiline('Teste',size=(90,5), key=('medias_estudo2') )],
	[sg.Multiline('Medias depois',size=(90,5), key=('medias_depois2') )],
	[sg.Button('COLOCOU AMOSTRA'), sg.Text('NÃO', key='ja_colocou_amostra')],
	#[sg.Button('ASTROM'), sg.Text('NÃO', key='astrom')],
	#[sg.Button('Reiniciar')],

	]


layout = [[sg.TabGroup([[sg.Tab('Principal', layout1), sg.Tab('Calibração', layout2)    ]] )],
			#[sg.Button('Botao geral')]
			]

# Janela
janela = sg.Window('Calorímetro').layout(layout)


		

	




