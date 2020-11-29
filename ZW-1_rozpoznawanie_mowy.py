import os
import time 
from time import sleep
import Adafruit_CharLCD as LCD
import w1thermsensor
import picamera
from picamera import PiCamera
import speech_recognition as sr
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = LCD.Adafruit_CharLCD(9, 11, 8, 7, 5, 6, 16, 2)
lcd.create_char(1,[7, 5, 7, 32, 32, 32, 32, 32])
lcd.clear()

def Komunikat_głosowy(tekst):
    os.system( 'espeak "'+tekst+'" --stdout -a 200 -s 180 -p 40 | aplay 2>/dev/null'  )

while True:

    r = sr.Recognizer()
    with sr.Microphone() as źródło_dźwięku:
        r.adjust_for_ambient_noise(źródło_dźwięku)
        try:
            print("Wydaj polecenie")
            wypowiedziane_słowo = r.listen(źródło_dźwięku)
            print("Przetwarzam ...")
            print("Polecenie: \n" + r.recognize_google(wypowiedziane_słowo, language="pl-PL"))
        except sr.UnknownValueError:
            print("Nie rozpoznałem polecenia")
            continue

    polecenie = r.recognize_google(wypowiedziane_słowo, language="pl-PL")
        
    if polecenie == "cześć":
        Komunikat_głosowy("Witaj")
                        
    if polecenie == "przedstaw się":
        Komunikat_głosowy("Nazywam się ZW-1, jestem asystentem cyfrowym, stworzył mnie Zygmunt Wypich")
 
    if polecenie == "co potrafisz":
        Komunikat_głosowy("Informuję o zdarzeniach za pomocą buzzera. Wyświetlam dane na wyświetlaczu LCD. Oświetlam otoczenie za pomocą diod LED. Mierzę aktualną temperaturę otoczenia. Odczytuję stan trzech przycisków ogólnego przeznaczenia. Wykrywam ruch w swoim otoczeniu. Łączę się z siecią Wi-Fi. Obserwuję otoczenie za pomocą kamery. Ciągle się uczę, więc moje umiejętności będą się powiększać") 
            
    if polecenie == "Pokaż datę":
        dzień = time.localtime().tm_mday
        miesiąc = time.localtime().tm_mon
        rok = time.localtime().tm_year                    
        GPIO.output(13, GPIO.HIGH)
        lcd.clear()
        lcd.message("Data:")
        if dzień < 10:
            lcd.set_cursor(0,1)
            lcd.message("0")
            dzień = str(dzień) 
            lcd.set_cursor(1,1)
            lcd.message(dzień + "/")
        else:
            dzień = str(dzień)
            lcd.set_cursor(0,1)
            lcd.message(dzień + "/")
        if  miesiąc < 10:
            lcd.set_cursor(3,1)
            lcd.message("0")
            miesiąc = str(miesiąc)
            lcd.set_cursor(4,1)
            lcd.message(miesiąc + "/")
        else:
            miesiąc = str(miesiąc)
            lcd.set_cursor(3,1)
            lcd.message(miesiąc + "/")
        rok = str(rok)
        lcd.set_cursor(6,1)
        lcd.message(rok)            
        Komunikat_głosowy("Polecenie zostało wykonane")
        sleep(5)
        lcd.clear()
        GPIO.output(13, GPIO.LOW)
            
    if polecenie == "Pokaż czas":
        godziny = time.localtime().tm_hour
        minuty = time.localtime().tm_min
        GPIO.output(13, GPIO.HIGH)
        lcd.clear()
        lcd.message("Czas:")
        if godziny < 10:
            lcd.set_cursor(0,1)
            lcd.message("0")
            godziny = str(godziny)
            lcd.set_cursor(1,1)
            lcd.message(godziny + ":")
        else:
            godziny = str(godziny)
            lcd.set_cursor(0,1)
            lcd.message(godziny + ":")
        if minuty < 10:
            lcd.set_cursor(3,1)
            lcd.message("0")
            minuty = str(minuty)
            lcd.set_cursor(4,1)
            lcd.message(minuty)
        else:
            minuty = str(minuty)
            lcd.set_cursor(3,1)
            lcd.message(minuty)            
        Komunikat_głosowy("Polecenie zostało wykonane")
        sleep(5)
        lcd.clear()
        GPIO.output(13, GPIO.LOW)
            
    if polecenie == "Pokaż temperaturę":
        GPIO.output(13, GPIO.HIGH)
        lcd.clear()
        sensor=w1thermsensor.W1ThermSensor()
        temp=sensor.get_temperature()
        temp=round(temp, 1)
        temperatura=str(temp)
        lcd.message('Temperatura:')
        lcd.set_cursor(0,1)
        lcd.message(temperatura + '\x01' + 'C')
        Komunikat_głosowy("Polecenie zostało wykonane")
        sleep(5)
        lcd.clear()
        GPIO.output(13, GPIO.LOW)
            
    if polecenie == "Włącz oświetlenie":
        GPIO.output(3, GPIO.HIGH)
        Komunikat_głosowy("Polecenie zostało wykonane")
            
    if polecenie == "Wyłącz oświetlenie":
        GPIO.output(3, GPIO.LOW)
        Komunikat_głosowy("Polecenie zostało wykonane")
            
    if polecenie == "zrób zdjęcie":
        Komunikat_głosowy("Za pięć sekund zaświecę diody LED, następnie zrobię zdjęcie, które zapiszę na pulpicie")
        sleep(5)
        GPIO.output(3, GPIO.HIGH)
        Kamera = PiCamera()
        Kamera.start_preview()
        Kamera.capture('/home/pi/Desktop/Zdjęcie.jpg')
        Kamera.stop_preview()
        Komunikat_głosowy("Polecenie zostało wykonane")
        GPIO.output(3, GPIO.LOW)
           
    polecenie = ""
















