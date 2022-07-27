#------------------------------ [IMPORT]------------------------------------
import network, time, urequests,utime
from machine import Pin, ADC, PWM, I2C,Timer
from ssd1306 import SSD1306_I2C
import framebuf
from utelegram import Bot

#--------------------------- [OBJETOS]---------------------------------------
#Pulso Cardiaco#
pulso = ADC(Pin(34))
pulso.atten(ADC.ATTN_11DB)
pulso.width(ADC.WIDTH_12BIT)

#Temperatura Corporal#
temperatura = ADC(Pin(32))
temperatura.atten(ADC.ATTN_11DB)
temperatura.width(ADC.WIDTH_12BIT)

#Bot Telegram#
TOKEN = '5432473846:AAGY1jC18a1pTebchYEKbj-qjxH0GvIC8xE'
bot = Bot(TOKEN)

#Led's#
#led_verde = Pin(19,Pin.OUT)
#led_rojo= Pin(18,Pin.OUT)

#IFTTT API#
url_telegram = "https://maker.ifttt.com/trigger/telegram/with/key/diBn9AFJo9opPYJ3uDuGKH?"
url_gmail = "https://maker.ifttt.com/trigger/Gmail/with/key/diBn9AFJo9opPYJ3uDuGKH?"
url_excel = "https://maker.ifttt.com/trigger/excel/with/key/diBn9AFJo9opPYJ3uDuGKH?"
url_mensaje = "https://maker.ifttt.com/trigger/mensaje/with/key/diBn9AFJo9opPYJ3uDuGKH?"
url_celular = "https://maker.ifttt.com/trigger/celular/with/key/diBn9AFJo9opPYJ3uDuGKH?"

#--------------------------- [FUNCION MAPEAR]----------------------------------------------------#
def mapear(valor_sensor, minimo_entrada, maximo_entrada, minimo_salida, maximo_salida):
  valor_mapeado = (valor_sensor - minimo_entrada) * (maximo_salida - minimo_salida) / (maximo_entrada - minimo_entrada) + minimo_salida
  return valor_mapeado

#--------------------------- [EJECUCION DEL CODIGO]------------------------------------------------#

#------------------------------[ CONECTAR WIFI ]---------------------------------------------------#
def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              
          miRed.active(True)                   
          miRed.connect(red, password)
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():      
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True
if conectaWifi ("Carluis_2Getb", "231189Pa"):
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    def ejecutar():
        
        while True:
            #led_rojo.value(0)
            #led_verde.value(1)
            valor_temperatura = temperatura.read()
            temperaura_mapeada=int(mapear(valor_temperatura, 0, 2000,0,100))
            
            valor_pulso = pulso.read()
            pulso_mapeado=int(mapear(valor_pulso, 0, 4095,0,100))
            
            print(valor_temperatura, end="\t")
            print(f"T:{temperaura_mapeada} Grados", end="\t")
            print(valor_pulso, end="\t")
            print(f"P:{pulso_mapeado} PPM")
            time.sleep(1)
            #-----------------------------------[IFTTT]------------------------------------------------------#
            if (temperaura_mapeada > 5000 or pulso_mapeado < 35):
                res_gmail = urequests.get(url_gmail+"&value1="+str(temperaura_mapeada)+"&value2="+str(pulso_mapeado)) 
                res_gmail.close ()
                
                res_telegram = urequests.get(url_telegram+"&value1="+str(temperaura_mapeada)+"&value2="+str(pulso_mapeado)) 
                res_telegram.close ()
                
                res_mensaje = urequests.get(url_mensaje+"&value1="+str(temperaura_mapeada)+"&value2="+str(pulso_mapeado)) 
                res_mensaje.close ()
                
                res_mensaje = urequests.get(url_mensaje+"&value1="+str(temperaura_mapeada)+"&value2="+str(pulso_mapeado)) 
                res_mensaje.close ()
                
                res_excel = urequests.get(url_excel+"&value1="+str(temperaura_mapeada)+"&value2="+str(pulso_mapeado)) 
                res_excel.close ()
                led_rojo.value(1)
                
                
            res_excel = urequests.get(url_excel+"&value1="+str(temperaura_mapeada)+"&value2="+str(pulso_mapeado)) 
            res_excel.close ()
        
    ejecutar() 

else:
    print ("Imposible conectar")
    miRed.active (False)
#------------------------------------[FIN DEL PROGRAMA]----------------------------------------------#