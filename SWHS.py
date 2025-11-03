#import python packages needed for program. 
import time
import sys
from threading import Timer

#allows a countdown to be visable on screen to the user. method is called in other methods - such as in an emergency. 
def countdown(t):
    while t > 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

#create new class SWHS
class SolarWaterHeatingSystem:

#initialising objects of class solarwaterheatingsystem
#to begin sensors read 0, pump and heater OFF. Valve ON as this can be made OFF in emergency modes.
    def __init__(self):
        self.ts1 = 0  #temperature sensor 1 (gas)
        self.ts2 = 0  #temperature sensor 2 (solar)
        self.pump = False
        self.heater = False
        self.valve = True

#method to simulate reading sensors
#obtain temperatures from user to simulate reading sensors.
#these inputs will be used to determine pump control, heater control and emergency mode. 
    def read_sensors(self):
        self.ts1 =float(input("Enter Temperature Sensor 1 (Gas): "))
        self.ts2 = float(input("Enter Temperature Sensor 2 (Solar): "))
            

#method for pump control. 
#If solar sensor reads more than 4, Pump ON. otherwise, OFF.
    def control_pump(self):
        if self.ts2 > 4:
            self.pump = True
        else:
            self.pump = False
    
#method for heater control. 
#If gas AND solar sensors read less than 4, or temp difference is more than 20, Heater ON. 
#otherwise, OFF.
    def control_heater(self):
        if (self.ts1 < 4 and self.ts2 < 4) or (self.ts1 - self.ts2 > 20):
            self.heater = True
        else:
            self.heater = False

#this is the optimization method, to maintain desired temp difference of 15.
#firstly, the current temp difference is calulated and depending on the input (temp difference), the output will be chosen by the system. 
#the system will loop between these until the desired temperature difference is met. 

    def optimize_temperature_difference(self):
        self.tempdifference = (self.ts1 - self.ts2) #calc for temp difference
        print("\nThe current temperature difference between tanks is:",self.tempdifference) #prints current temp difference

#if temp difference is 20 or higher, gas heater will be on and pump speed increased
        if self.tempdifference >= 20 : #too high
            print("\nAlert: Temperature difference between tanks is too high.")
            time.sleep(0.5) #simulate time for igniting gas
            print("Gas heater ignited. Increasing pump flow rate to heat up water in solar tank...")

#while temp difference is 20 or higher, the solar temp will increase to decrease the temp difference. 
        while self.tempdifference >= 20: 
            self.ts2 +=1 #increase solar temp
            self.tempdifference -=1 #decrease temp difference
            print("\nGas temp is:",self.ts1,   "Solar temp is:",self.ts2) #prints new gas and solar temps
            print("Temperature difference is:",self.tempdifference) #prints new calculated temp difference

#while temp difference is between 16 and 19, the pump be on but it should slow to decrease gas temp.
        if self.tempdifference >=16 <=19:
            print("\nAlert: Temperature difference between tanks is too high.")
            time.sleep(0.5) # simulate time for slowing pump
            print("Slowing pump flow rate to decrease gas temp...")

#while temp difference is between 16 and 19, the gas temp will decrease to decrease the temp difference. 
        while self.tempdifference >=16 <=19:
            self.ts1 -=1  #decrease gas temp
            self.tempdifference -=1 #decrease temp difference
            print("\nGas temp is:",self.ts1,   "Solar temp is:",self.ts2) #prints new gas and solar temps
            print("Temperature difference is:",self.tempdifference) #prints new calculated temp difference

#if temp difference is under 15, the pump will be on but speed should increase to raise gas temp.
        if self.tempdifference < 15:
            print("\nAlert: Temperature difference between tanks is too low.")
            time.sleep(0.5) #simulate time for increasing pump speed
            print("Increasing pump flow rate to increase gas temp...")

#while temp difference is under 15, increase gas temp to increase the temp difference.
        while self.tempdifference < 15:
            self.ts1 +=1  #increase gas temp
            self.tempdifference +=1 #increase temp difference
            print("\nGas temp is:",self.ts1,   "Solar temp is:",self.ts2) #prints new gas and solar temps
            print("Temperature difference is:",self.tempdifference) #prints new calculated temp difference

#if temp difference is equal to 15, pump on but heater off. pump should maintain current flow from this point.       
        if self.tempdifference == 15:
             print("\nAlert: Temperature difference between tanks is correct.")
             time.sleep(0.5) #simulate maintaining pump speed
             print("Maintaining current pump flow rate to maintain temperatures...")
             self.pump = True
             self.heater = False

#if gas hits 70 or over, enter emergency state. timer displayed. 
    def handle_overheating(self):
        if self.ts1 >=70:
            print("\nEmergency: Gas Water Boiler Tank Overheating")
            t = 6  #timer set to 6 seconds for testing pursposes. will be 10 mins in real life.
            countdown(int(t)) #display timer
            

#while gas is 70or over, decrease gas temp. 
#stop all functions and set timer. 
#after timer, issue will be fixed. valve will be true to continue system.
        while self.ts1 >= 70:
            self.ts1 -=1 #decrease gas
            self.valve = False
            self.pump = False
            self.heater = False
            print("\nReducing Gas Temperature...",self.ts1)
            time.sleep(0.5) #simulate reducing gas temp
            self.valve = True

#manual stop is triggered if user enters STOP. 
#stop all functions and timer set. 
    def handle_leakage(self):
        time.sleep(0.5)
        #whilst program is maintaining desired temp difference, allow user to enter manual emegerncy mode or return to start
        manual_stop = input("\nEnter 'STOP' to simulate manual stop due to leakage. \nSelect ENTER to return to start. ")
        if manual_stop == 'STOP': #if user enters stop, turn off all functions
            self.valve = False
            self.pump = False
            self.heater = False
            print("Emergency: Leakage in the system")
            t = 6  #timer set to 6 seconds for testing purposes. 30 min real life.
            countdown(int(t))
#check with user if resolved. if yes, valve will be true to continue system. while no, timer and confirmation for resolution will loop until user selects yes. 
            check_resolved = input("\nPlease confirm if the issue is fixed? (YES/NO) :  ")
            if check_resolved == 'YES':
                self.valve = True
            while check_resolved == 'NO':
                t = 6  #timer. set to 6 seconds for testing purposes. 30 min real life.
                countdown(int(t))
                 

# method to display current status (pump & heater ON or OFF and temp difference)
    def display_status(self):
        time.sleep(0.5)
        print(f"\nTS1: {self.ts1}°C, TS2: {self.ts2}°C")
        print(f"Pump: {'ON' if self.pump else 'OFF'}, Heater: {'ON' if self.heater else 'OFF'}")
        print("Temperature difference:",self.tempdifference)

#method to allow continuous looping until desired temp is reached. at this point, new temp readings can be entered if user selects Enter and the system will re-loop.
    def run(self):
        while True: #call all methods in order. 
            self.read_sensors()
            self.control_pump()
            self.control_heater()
            self.handle_overheating()
            self.optimize_temperature_difference()
            self.display_status()
            self.handle_leakage()
            time.sleep(0.3)  # simulate time delay for the next cycle

#method to run SWHS system.
if __name__ == "__main__":
    system = SolarWaterHeatingSystem()
    system.run()
