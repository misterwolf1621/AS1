"""Hauptfunktion zur Ansteuerung eines RC-Modells mithilfe des Raspberry Pi.
"""

__email__ = "teamprojekt@tuhh.de"
__copyright__ = "Technische Universitaet Hamburg, Institut fuer Kunststoffe und Verbundwerkstoffe"
__version__ = "2023.1.0"

from esc import Esc
from servo import Servo
from dev import Controller
import time
import pigpio

def main():
    print("Software up and running")
    
    #Erstellung zweier Servos auf Pin 12 und 13
    servoLeft = Servo(12,0,180,90,0,False)
    servoRight = Servo(13, 0, 180, 90, 0, False)
    
    #led = pigpio.pi()
    

    #Erstellung zweier Motoren
    engineLeft = Esc(5)
    engineRight = Esc(6)
    
    

    #Erstellung X-Box Controller
    ctrl = Controller()

    trimServoRight = 0
    trimServoLeft = -2
    trimSpeedLeft = -0.1
    trimSpeedRight = 0.1
    reset = False

    for event in ctrl.dev.read_loop(): 
            #print(f"{event.code} code")

        if(event.code == ctrl.BTN_A):
            if(event.value == 1):
                if(reset == False):
                    engineLeft.esc_write(1500)
                    engineRight.esc_write(1500)
                    servoLeft.servo_write(88)
                    servoRight.servo_write(90)
                    trimServoLeft = 88
                    trimServoRight = 90
                    reset = True
        
        elif(event.code == ctrl.BTN_LB):
            if(event.value == 1):
                #verwendung von reverse Thrust, wegen Drehbarkeit um maximal 180°
                #servoLeft.servo_write(90)
                #servoRight.servo_write(90)

                #Schub des positiven Propellers auf 64% begrenzt, da der Vorschub in negative Richtung 64% des Vorschubes in positive Richtung beträgt

                #propSpeedLeft = 1500 - 500 * (ctrl.ABS_LT / 1023)
                #propSpeedRight = 1500 + 500 * (ctrl.ABS_LT / 1023)
                
                if(reset):
                    engineLeft.esc_write(1300)
                    engineRight.esc_write(1260)
                    #Abweichung 20%
               
                    
            else:
                engineLeft.esc_write(1500)
                engineRight.esc_write(1500)
                

        elif(event.code == ctrl.BTN_RB):
            if(event.value == 1):
                #verwendung von reverse Thrust, wegen Drehbarkeit um maximal 180°
                #servoLeft.servo_write(90)
                #servoRight.servo_write(90)
                if(reset):
                    engineLeft.esc_write(1740)
                    engineRight.esc_write(1700)
                    #Abweichung 20%
            else:
                engineLeft.esc_write(1500)
                engineRight.esc_write(1500)
        #Schub geben

        elif(event.code == ctrl.ABS_RT):
            #Umwandlung LT zu PWM Speed
            propSpeed = 500 * (event.value / 1023)

            if(propSpeed > 50):
                speedLeft = 1500 - propSpeed * (1 + trimSpeedLeft)
                speedRight = 1500 + propSpeed * (1 + trimSpeedRight) + 5
            else:
                speedLeft = 1500
                speedRight = 1500
            if(speedLeft > 2000):
                speedLeft = 2000
            elif(speedLeft < 1000):
                speedLeft = 1000

            if(speedRight > 2000):
                speedRight = 2000
            elif(speedRight < 1000):
                speedRight = 1000 

            engineLeft.esc_write(speedLeft)
            engineRight.esc_write(speedRight)

            #print(speedLeft)
            #print(speedRight)

            reset = False

        elif(event.code == ctrl.ABS_LT):
            #Umwandlung LT zu PWM Speed
            propSpeed = 500 * (event.value / 1023)
            if(propSpeed > 50):
                speedLeft = 1500 + propSpeed * (1 + trimSpeedRight) 
                speedRight = 1500 - propSpeed * (1 + trimSpeedLeft) - 5

            else:
                speedLeft = 1500
                speedRight = 1500

            if(speedLeft > 2000):
                speedLeft = 2000
            elif(speedLeft < 1000):
                speedLeft = 1000

            if(speedRight > 2000):
                speedRight = 2000
            elif(speedRight < 1000):
                speedRight = 1000 
            

            engineLeft.esc_write(speedLeft)
            engineRight.esc_write(speedRight)

            #print(speedLeft)
            #print(speedRight)

            reset = False
        #Trimmung:
        elif(event.code == ctrl.ABS_DX):
            trimSpeedLeft = trimSpeedLeft + 0.1 * event.value
            trimSpeedRight = trimSpeedRight + 0.1 * event.value

        #UP&Down

        elif(event.code == ctrl.ABS_LSY):

            moduledInputLeft = event.value - 32737

            trimServoLeft = trimServoLeft + 5 * (moduledInputLeft/ 33000)

            moduledInputRight = event.value - 32737

            trimServoRight = trimServoRight - 5 * (moduledInputRight/ 33000)

            #max: 65534

            if(trimServoLeft > 180):
                trimServoLeft = 180
            elif(trimServoLeft < 0):
                trimServoLeft = 0

            if(trimServoRight > 180):
                trimServoRight = 180
            elif(trimServoRight < 0):
                trimServoRight = 0

            servoLeft.servo_write(trimServoLeft)
            servoRight.servo_write(trimServoRight)

            #print(trimServoLeft)
            #print(event.value)

            #print(event.code)

            reset = False
    

if __name__ == "__main__":
    main()



#Erstellt von einer künstlichen Inteligenz:

'''
Ja, die Syntax in Ihrem Python-Code sieht korrekt aus. Es handelt sich um eine Steuerungsfunktion für ein RC-Modell, die auf einem Raspberry Pi läuft.
Der Code verwendet verschiedene Module wie "esc", "servo" und "dev" sowie die Zeitbibliothek ("time"). 
Der Code enthält auch eine Endlosschleife (while True:), die die Hauptfunktionalität für die Ansteuerung des RC-Modells implementiert.

Hier sind einige Punkte zur Syntax und zum Code-Stil:

Kommentare: Gute Verwendung von Kommentaren, die den Code erklären und die verschiedenen Abschnitte kennzeichnen.
Einrückung: Die Einrückung ist konsistent und entspricht den Python-Standards (normalerweise vier Leerzeichen pro Einrückungsstufe).
Variablennamen: Die meisten Variablennamen sind aussagekräftig und folgen den Python-Standards.
Modulimporte: Die verwendeten Module ("esc", "servo", "dev") werden korrekt importiert.
Es ist wichtig zu beachten, dass die Endlosschleife (while True:) dazu führt, dass das Programm unendlich läuft, es sei denn, es wird durch eine externe Aktion 
(z. B. Benutzerunterbrechung) beendet.

Wenn Sie spezifische Fragen oder Anpassungen haben, lassen Sie es mich wissen!

'''