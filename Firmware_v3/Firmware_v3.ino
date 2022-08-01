
#include "Arduino.h"
#include <INA.h>                  // Biblioteca Zanshin INA https://github.com/Zanduino/INA/wiki
#include "Nanoshield_Termopar.h"  //Biblioteca termopar https://github.com/circuitar/Nanoshield_Termopar
#include <Wire.h>
#include "max6675.h"        //https://github.com/adafruit/MAX6675-library
#include <EEPROM.h>


/* Variávris para sensor de corrente e impressão*/
const uint32_t SHUNT_MICRO_OHM{2000};  // Resistencia shunt resistance em  MicroOhm. 100000 é 0.1 Ohm
const uint16_t MAXIMO_AMPERE{15};          // Maximo valor de corrente do sensor
uint8_t        devicesFound{0};          
INA_Class      INA;                      
unsigned long leituras=0;
unsigned long tempo_atual = micros();;   //tempo em microsegundos desde que o programa comecou - dá overflow em 70 minutos
unsigned long tempo_anterior = micros();;
float leitura_tensao, leitura_corrente, tempo_conversao;
double integrador_energia=0.0;

bool SAIDA_MANUAL = false;
bool ASTROM = false;
int saida_manual_valor = 0;

/*para o segundo termopar - ele consome pouca corrente 1.6mA, o pino do arduino consegue alimentar*/
int gnd_termopar = 22;
int alimentacao_termopar = 24;
int termopar_sck_pin = 26;
int termopar_cs_pin  = 28;
int termopar_so_pin  = 30;

static char buffKP[10], buffKI[10], buffKD[10]; 
float k;
  
MAX6675 termopar(termopar_sck_pin, termopar_cs_pin, termopar_so_pin);

  int LEITURAS_POR_CICLO=125;
  //double Output;
  double lastErr;
  double errSum=0;
  unsigned long lastTime;
  double divisor=10;
  double minOut=0;
  double maxOut=LEITURAS_POR_CICLO;
  //double Setpoint;


   int endereco_kp_eeprom=0;
   int endereco_ki_eeprom=3;
   int endereco_kd_eeprom=6;

//FIM PID MANUAL





/*Variáveis de entrada do algoritmo PID. KP é o proporcional. KI o integrativo e Kd o derivativo. Alterar esses valores pode melhorar o ajuste da curva de aquecimento*/
#define KP  19.48//39.75
#define KI  54
#define KD  10.5

/*esse valor estabilizou, mas oscila muito depois a energia
#define KP  59.6
#define KI  7.91
#define KD  5.81

/* variou - diminuir kp (ficou pior com 0.5)
#define KP  1.087
#define KI  32
#define KD  8
/*
#define KP  0.1
#define KI  0
#define KD  0.0
/*
#define KP  0.15
#define KI  87
#define KD  21.75

/*oscilou +-15graus
#define KP  0.15
#define KI  43
#define KD  0.0


/* remember - calibrado pelo pid do site, com varios valores, mas ficou variano ao redor de 10 graus, mas nao ficou ruim. Nao fica ligando 100% e depois zero*/
/* Fica variando mas permitir leituras #define KP  0.132
#define KI  49.87
#define KD  6.71

/*
//pelo metodo do ziegler - ruim, demora mto
#define KP  0.024
#define KI  128
#define KD  32

/*
//pelo metodo de cohen-coon
#define KP  8.413
#define KI  153.34
#define KD  23.24

/*
//calibrado pelo metodo do paper(skogestad), usando valores de delta y inf. Caiu 12 graus e 
#define KP  0.0297
#define KI  99.2
#define KD  0


*/

/* Variáveis para termopar e PID*/
#define PINO_SAIDA 25       //Saída da carga
double Setpoint=-10, Input=0, Output=0, saida_pwm_manual=0;  

double Kp = KP, Ki = KI, Kd = KD;




Nanoshield_Termopar tc(45, TC_TYPE_K, TC_AVG_OFF);
float temperatura_atual=0, temperatura_atual2=0;
float temperatura_ambiente;

int tempo_ligado=0,tempo_exibir_dados=1000;
long temp=5;
unsigned long tempo_atual_pwm = millis(); 
unsigned long tempo_anterior_pwm = millis();
unsigned long  tempo_atual_leitura=0, tempo_anterior_leitura=0; 
int INTERVALO_PWM_MANUAL = 1990;  //tempo que chama o pwm em milisegundos
boolean LIGADO=false;

int INTERVALO_leitura = 1990;  //milissegundos - estava 1990

//variáveis para medias
float MEDIA_tempo_conversao=0, MEDIA_temperatura=0,  MEDIA_corrente=0, MEDIA_tensao=0;   
int contagem_para_media=0;
int astrom_valor=0;
int limite_saida = LEITURAS_POR_CICLO;
int contar_PID_ate_LEITURAS_POR_CICLO=0; 

void setup() {
  Serial.begin(115200);
  pinMode(PINO_SAIDA, OUTPUT);
  
  /* Inicia o sensor de corrente*/
  devicesFound = INA.begin(MAXIMO_AMPERE, SHUNT_MICRO_OHM, INA260);  
  while (devicesFound == 0) {
    Serial.println(F("Não encontrou sensor de corrente, testando novamente em 10 segundos..."));
    delay(10000);                                             
    devicesFound = INA.begin(MAXIMO_AMPERE, SHUNT_MICRO_OHM, INA260);  
  } 
  
  /* Configurações do sensor de corrente*/                                                          
  INA.setBusConversion(8500);             // Tempo máximo de conversão de 8.244ms
  INA.setShuntConversion(8500);           // Tempo máximo de conversão de 8.244ms
  INA.setAveraging(1);                  // Média de leituras antes de dar resultado. Com 4 aproximadamente 66ms cada leitura 
  INA.setMode(INA_MODE_CONTINUOUS_BOTH);  // Bus/shunt medido continuamente

//termopar 2 alimentação
  pinMode(alimentacao_termopar, OUTPUT); 
  pinMode(gnd_termopar, OUTPUT); 
  digitalWrite(alimentacao_termopar, HIGH);
  digitalWrite(gnd_termopar, LOW);



  /* Inicia Termopar e PID */
  tc.begin();
  tc.read();
  Setpoint = temp;
              

  /*Imprime configuracoes atuais PID no software*/
              Serial.print("P:");
               dtostrf(Kp, 7, 2, buffKP);
               Serial.print(buffKP);
               dtostrf(Ki, 7, 2, buffKI);
               Serial.print("I:");
               Serial.print(buffKI);
               dtostrf(Kd, 7, 2, buffKD);
               Serial.print("D:");
               Serial.print(buffKD); 
               Serial.print("\n");




  
}  // fim setup()

void Imprime_erro_termopar() { 
  if (tc.isOpen()) {Serial.print("(Circuito aberto) \n");  } 
  else if (tc.isOverUnderVoltage()) {Serial.print("(Sub/supertensao) \n"); } 
  else if (tc.isInternalOutOfRange()) {Serial.print("(Temperatura interna fora de valor) \n");  } 
  else if (tc.isExternalOutOfRange()) {Serial.print("(Temperatura externa fora de valor) \n"); }
  }





void loop() {
 tempo_atual_leitura = millis();


 
/* Função chamada sempre que leitura termina. Le os sensores e é a saida do PWM para que seja no periodo da leitura*/
if (INA.conversionFinished(0)){
    contagem_para_media++;
    
    leitura_tensao = (float)INA.getBusMilliVolts(0)/1000;
    if (INA.getBusMicroAmps(0) >=0){
        leitura_corrente = (float)INA.getBusMicroAmps(0)/1000;   }
    else{ leitura_corrente = 0.0; }
    
    MEDIA_corrente = MEDIA_corrente + leitura_corrente;
    MEDIA_tensao = MEDIA_tensao + leitura_tensao;
    
    tempo_atual_pwm = millis();
    tempo_atual=micros();
    tempo_conversao = (float)(tempo_atual-tempo_anterior)/1000;
    MEDIA_tempo_conversao = tempo_conversao + MEDIA_tempo_conversao ;
    
    /* acontece quando deu overflow do micros() - somente perde a leitura do overflow */
    if(tempo_anterior>tempo_atual){ tempo_conversao = (float)(tempo_atual)/1000;  }
     tempo_anterior = tempo_atual;


       /* Calcula a energia no período */
    integrador_energia = integrador_energia + (leitura_tensao*leitura_corrente*tempo_conversao)/1000;


    /* Controle da saída PWM manual, dentro do loop da leitura */
    
    
    
    //if ((tempo_atual_pwm <tempo_anterior_pwm+tempo_ligado) && LIGADO==true){ digitalWrite(PINO_SAIDA, HIGH);      }
    //    else {digitalWrite(PINO_SAIDA, LOW);  }

    if (float(contar_PID_ate_LEITURAS_POR_CICLO) < saida_pwm_manual && LIGADO==true ){  digitalWrite(PINO_SAIDA, HIGH);   }
    else {digitalWrite(PINO_SAIDA, LOW);  }
/*Imprime para o usuario os valores e zera o integrador de energia*/
    if (contar_PID_ate_LEITURAS_POR_CICLO>LEITURAS_POR_CICLO-1) {  
        
        /* leitura do termopar*/
        tc.read(); //le o termopar
        if (tc.hasError()) { Imprime_erro_termopar();  } 
      
       // temperatura_atual2 = termopar.readCelsius();
        temperatura_atual = tc.getExternal();
        temperatura_ambiente=tc.getInternal();

        
    
        MEDIA_tempo_conversao = MEDIA_tempo_conversao; 
        MEDIA_corrente = MEDIA_corrente/contagem_para_media;    
        MEDIA_tensao = MEDIA_tensao/contagem_para_media;    
    
        static char buff[250], bufftensao[12], buffcorrente[12], bufftempo[11], bufftemperatura[10],bufftemp2[10], buffpwm[10], buffleituras[10], buffenergia[50];
        dtostrf(MEDIA_corrente, 9, 4, buffcorrente);
        dtostrf(MEDIA_tempo_conversao, 10, 3,  bufftempo);
        dtostrf(MEDIA_tensao, 8, 3, bufftensao);
        dtostrf(temperatura_atual, 8, 2, bufftemperatura);
        dtostrf(saida_pwm_manual, 8, 2, buffpwm);
        dtostrf(leituras, 8, 0, buffleituras);
        dtostrf(integrador_energia, 9, 2, buffenergia);
        //dtostrf(temperatura_atual2, 9, 2, bufftemp2);
        dtostrf(temperatura_ambiente, 9, 2, bufftemp2);
    
        sprintf(buff, "L%s Tensao V:%s,Corrente mA:%s, tempo de conversao:%s, saída pwm:%s, leitura:%s, integracao energia: %s, temperatura 2: %s\n", bufftemperatura, bufftensao, buffcorrente, bufftempo, buffpwm, buffleituras, buffenergia, bufftemp2) ; //falta colocar output
        Serial.print(buff);
    
        leituras++;

        integrador_energia=0;
        contagem_para_media=0;
        MEDIA_tempo_conversao = 0; 
        MEDIA_temperatura = 0; 
        MEDIA_corrente = 0;    
        MEDIA_tensao = 0;
        
    
        /***********COMECO DO CALCULO PID*************************************************************/

        // Calcula a diferença de tempo para o diferencial
        unsigned long now = millis();
        double timeChange = (double)(now - lastTime);
        timeChange=timeChange/1000;  //converte para segundos
        // Calculata erro, P, I e D 
        double error = Setpoint - temperatura_atual;
        errSum += error * timeChange;
        double dErr = (error - lastErr) / timeChange;

        // Calcula a saida pelo artigo Vance
        double newOutput = Kp*(error + (1/Ki)*errSum + Kd*dErr);
        Serial.print("Saida PID:"); Serial.print(newOutput); Serial.print("\n");
        //Serial.print( "temp ambiente");
        //Serial.print(tc.getInternal());
        //Serial.print( "\n");
        
        // Modula valores de saida
        if (newOutput>LEITURAS_POR_CICLO) { Output = LEITURAS_POR_CICLO;  
        //ZERAR O INTEGRATIVO PARA NÃO TER PICO GIGANTE
        errSum =0;
        } 
        else if (newOutput<0) { Output = 0;  } 
        else {  Output = newOutput;   }

        // Atualiza variaveis
        lastErr = error;
        lastTime = now;

      /**********************FIM DO CÁLCULO DO PID*************************************************************/
      //FIM DO PID -- OUTPUT é a saída

        if (SAIDA_MANUAL == true){
           saida_pwm_manual = saida_manual_valor;
        }
        else if (ASTROM== true){
          if (temperatura_atual<astrom_valor){ saida_pwm_manual = LEITURAS_POR_CICLO; }
          else{ saida_pwm_manual=0;     }        
        }      
        else { 
          if (Output>limite_saida){ saida_pwm_manual = limite_saida;      }
          else{ saida_pwm_manual = Output; }
         }

         if (saida_pwm_manual>limite_saida){saida_pwm_manual=limite_saida; }
        contar_PID_ate_LEITURAS_POR_CICLO=0;
        //tempo_anterior_pwm = tempo_atual_pwm;
        //tempo_ligado = (saida_pwm_manual*INTERVALO_PWM_MANUAL)/255;
        
     }
   contar_PID_ate_LEITURAS_POR_CICLO++;
} //FICOU AQUI


/* Recebe os comandos do software*/
if (Serial.available() > 0) {
       
    char leitura = Serial.read(); // Variavel que receberá os valores enviados pelo programa em python
    temp = Serial.parseInt();
    
    
    switch (leitura) {
          
            case 'T':
            Serial.print("SETAR TEMPERATURA ");
            Setpoint=temp;
            Serial.print(temp);
            Serial.print("\n");
            errSum=0;
            if(temp<2){LIGADO = false;}
            else {LIGADO = true;}
            break;   

            case 'L':
            Serial.print("TEMPO PARA EXIBIR DADOS ");
            tempo_exibir_dados=temp;
            Serial.print(temp);
            Serial.print("\n");
            break;

          //se receber M muda saida para manual

           case 'M':
            Serial.print("ARDUINO: SAIDA MANUAL");
            SAIDA_MANUAL = true;
            LIGADO = true;
            saida_manual_valor = temp;
            Serial.print(saida_manual_valor);
            Serial.print("\n");
            break;

            case 'Z':
            
            if (ASTROM){
              LIGADO = false;
              ASTROM = false;
              saida_pwm_manual=0;
              Serial.print("ARDUINO: ASTROM DESLIGADO");
              }
            else{
            LIGADO = true;
            ASTROM = true;
            astrom_valor=temp;
            Serial.print("ARDUINO: ASTROM LIGADO");
            //Serial.print(astrom_valor);
            }
          
            break;


            //LIMITE DE SAIDA
            case 'Y':
            limite_saida=temp;
            Serial.print("O Limite de Saida:");
            Serial.print(limite_saida);
            Serial.print("\n");
            break;
            
            case 'S':
            Serial.print("KP LIDO EEPROM");
            //EEPROM.put(endereco_kp_eeprom, highByte(float(Kp)));  
            //EEPROM.put(endereco_kp_eeprom+1, lowByte(float(Kp))); 
           
            Serial.print("KP LIDO EEPROM");
            //Serial.print(word(EEPROM.read(endereco_kp_eeprom), EEPROM.read(endereco_kp_eeprom +1)));  
                  
            break;

          //Se receber A muda saida para automatica do PID
          case 'A':
            Serial.print("ARDUINO: SAIDA AUTOMATICA PID\n");
            SAIDA_MANUAL = false;
            LIGADO = false;
            
            break;


            case 'P':
            //Serial.print(temp);
               Kp = float(temp/1000.0);
               //Serial.print(myPID.GetKp());
              //COMENTEI myPID.SetTunings(Kp, Ki, Kd); 
               //Serial.print(myPID.GetKp()); 
                 
            break;
            
            
            case 'I':
             Ki = float(temp/1000.0);
             if (Ki==0){Ki=0.01;} //evitar divisao por 0
               //Serial.print(myPID.GetKi());
              //COMENTEI myPID.SetTunings(Kp, Ki, Kd); 
               //Serial.print(myPID.GetKi());           
            break;


            case 'D':
             Kd = float(temp/1000.0);
               //Serial.print(myPID.GetKd());
             //COMENTEI  myPID.SetTunings(Kp, Ki, Kd); 

               
               
               
              
               Serial.print("P:");
             //  k = myPID.GetKp();
               k=Kp;
               dtostrf(k, 7, 2, buffKP);
               Serial.print(buffKP);
              // k=myPID.GetKi();
              k=Ki;
               dtostrf(k, 7, 2, buffKI);
               Serial.print("I:");
               Serial.print(buffKI);
               //k=myPID.GetKd();
               k=Kd;
               dtostrf(k, 7, 2, buffKD);
               Serial.print("D:");
               Serial.print(buffKD); 
               Serial.print("\n");

                      
            break;
            
                  
          }
    }




}  //fim do loop
