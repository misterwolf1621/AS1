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
    trimServoLeft = 0
    trimSpeedLeft = 0
    trimSpeedRight = 0
    mode = "norm"

    for event in ctrl.dev.read_loop(): 

            if(event.code == ctrl.BTN_A):
                if(event.value == 1):
                    print("A Pressed")
                    mode = "norm"

            if(event.code == ctrl.BTN_LB):
                if(event.value == 1):
                    #verwendung von reverse Thrust, wegen Drehbarkeit um maximal 180°
                    servoLeft.servo_write(90 + trimServoLeft)
                    servoRight.servo_write(90 + trimServoRight)

                    #Schub des positiven Propellers auf 64% begrenzt, da der Vorschub in negative Richtung 64% des Vorschubes in positive Richtung beträgt

                    propSpeedLeft = 1500 - 500 * (ctrl.ABS_LT / 1023)
                    propSpeedRight = 1500 + 320 * (ctrl.ABS_LT / 1023)

                    engineLeft.esc_write(propSpeedLeft)
                    engineRight.esc_write(propSpeedRight)

            if(event.code == ctrl.BTN_RB):
                if(event.value == 1):
                    #verwendung von reverse Thrust, wegen Drehbarkeit um maximal 180°
                    servoLeft.servo_write(90 + trimServoLeft)
                    servoRight.servo_write(90 + trimServoRight)

                    #Schub des positiven Propellers auf 64% begrenzt, da der Vorschub in negative Richtung 64% des Vorschubes in positive Richtung beträgt

                    propSpeedRight = 1500 - 500 * (ctrl.ABS_LT / 1023)
                    propSpeedLeft = 1500 + 500 * (ctrl.ABS_LT / 1023)

                    engineLeft.esc_write(propSpeedLeft)
                    engineRight.esc_write(propSpeedRight)

            if(event.code == ctrl.ABS_LT):
                #Umwandlung LT zu PWM Speed
                propSpeed = 1500 + 500 * (event.value / 1023)

                speedLeft = propSpeed + trimSpeedLeft
                speedRight = propSpeed + trimSpeedRight

                if(speedLeft > 2000):
                    speedLeft = 2000

                if(speedRight > 2000):
                    speedRight = 2000

                engineLeft.esc_write(speedLeft)
                engineRight.esc_write(speedRight)

                

            if(event.code == ctrl.ABS_RT):
                #Umwandlung LT zu PWM Speed
                propSpeed = 1500 - 500 * (event.value / 1023)

                speedLeft = propSpeed + trimSpeedLeft
                speedRight = propSpeed + trimSpeedRight

                if(speedLeft < 1000):
                    speedLeft = 1000

                if(speedRight < 1000):
                    speedRight = 1000

                engineLeft.esc_write(speedLeft + trimSpeedLeft)
                engineRight.esc_write(speedRight + trimSpeedRight)

            if(event.code == ctrl.ABS_DX):
                trimSpeedLeft = trimSpeedLeft + 5 * event.value
                trimSpeedRight = trimSpeedRight - 5 * event.value

            if(event.code == ctrl.ABS_LSX):
                

                if(trimServoLeft > 180):
                    trimServoLeft = 180
                elif(trimServoLeft < 0):
                    trimServoLeft = 0
                
                trimServoLeft = trimServoLeft + (event.value / 32727) * 180

                if(trimServoRight > 180):
                    trimServoRight = 180
                elif(trimServoRight < 0):
                    trimServoRight = 0

                trimServoRight = trimServoRight + (event.value / 32727) * 180

                servoLeft.servo_write(trimServoLeft)
                servoRight.servo_write(trimServoRight)
            #print(event.code)
    
    '''
    while True:
        
        #led.write(45, 1)

        ctrl.read_loop()
        
        print(f"a:{ctrl.BTN_A.value()}; b:{ctrl.BTN_B};{ctrl.BTN_X};{ctrl.BTN_Y};")        
        if(ctrl.BTN_A == 1):
            #ctrl.rumble()
            mode = "norm"
        if(ctrl.BTN_X == 1):
            #ctrl.rumble()
            mode = "l-turn"
        if(ctrl.BTN_B == 1):
            #ctrl.rumble()
            mode = "r-turn"
        if(ctrl.BTN_Y == 1):
            mode = "rev"


        if(mode == "norm"):
            

            #Input Stick Links/Rechts

            inputStickX = ctrl.ABS_LSX # zwischen +- 32767
            inputStickY = ctrl.ABS_LSY # zwischen +- 32767

            servoPosLeft = (inputStickY / 32767) * 90 + 90 + trimServoLeft

            #Begrenzer links
            if(servoPosLeft < 0):
                servoPosLeft = 0
            if(servoPosLeft > 180):
                servoPosLeft = 180

            servoPosRight = (inputStickY / 32767) * 90 + 90 + trimServoRight

            #Begrenzer rechts
            if(servoPosRight < 0):
                servoPosRight = 0
            if(servoPosLeft > 180):
                servoPosRight = 180

            servoLeft.servo_write(servoPosLeft)
            servoRight.servo_write(servoPosRight)

            #Geschwindigkeit Motoren

            

            # Beide Motoren laufen üblicherweise bei halber eingestellter Leistung über ABS_LT
            # Wenn der Stick bewegt wird, bekommt einer mehr der andere weniger, sodass bei vollausschlag einer bei 100% läuft, der andere gar nicht


            time.sleep(1)
        
        if(mode == "rev"):
            #Umwandlung LT zu PWM Speed
            propSpeed = 1500 - 500 * (ctrl.ABS_LT / 1023)

            #Input Stick Links/Rechts

            inputStickX = ctrl.ABS_LSX # zwischen +- 32767
            inputStickY = ctrl.ABS_LSY # zwischen +- 32767

            servoPosLeft = (inputStickY / 32767) * 90 + 90 + trimServoLeft

            #Begrenzer links
            if(servoPosLeft < 0):
                servoPosLeft = 0
            if(servoPosLeft > 180):
                servoPosLeft = 180

            servoPosRight = (inputStickY / 32767) * 90 + 90 + trimServoRight

            #Begrenzer rechts
            if(servoPosRight < 0):
                servoPosRight = 0
            if(servoPosLeft > 180):
                servoPosRight = 180

            servoLeft.servo_write(servoPosLeft)
            servoRight.servo_write(servoPosRight)

            #Geschwindigkeit Motoren

            speedLeft = propSpeed / 2 + ((propSpeed / 2) * inputStickX / 32767)
            speedRight = propSpeed / 2 - ((propSpeed / 2) * inputStickX / 32767)

            engineLeft.esc_write(speedLeft)
            engineRight.esc_write(speedRight)

            # Beide Motoren laufen üblicherweise bei halber eingestellter Leistung über ABS_LT
            # Wenn der Stick bewegt wird, bekommt einer mehr der andere weniger, sodass bei vollausschlag einer bei 100% läuft, der andere gar nicht


            time.sleep(1)

        if(mode == "l-turn"):

            

            time.sleep(1)
        
        if(mode == "r-turn"):

            

            time.sleep(1)
    #pass
    '''

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