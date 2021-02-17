import time
import os
import sys, getopt
import RPi.GPIO as GPIO

directory = 'controller'

if not os.path.exists(directory):
    os.makedirs(directory)

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
inputpins = []

# Read in the parameters
def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hp:",["pins="])
   except getopt.GetoptError:
      print 'missing parameters: -p <pin> <pin>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'gpio_pwm.py -p <pin> <pin>'
         sys.exit()
      elif opt in ("-p", "--pins"):
         inputpins.append(arg)
      else:
         print 'gpio_pwm.py -p <pin> <pin>'
         sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])

# Use the parameters and set gpio   
if(len(inputpins)>0):   
   print 'pin list:', str(inputpins)

   for pinNumber in inputpins:
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(int(pinNumber), GPIO.OUT)
      
      p = GPIO.PWM(int(pinNumber), 50)  # frequency=50Hz
      filename = "%s/pin%s.running" % (directory, pinNumber)
      f = open(filename, "w")

      p.start(0)
      try:
         while(1):
            for dc in range(0, 101, 1):
                  p.ChangeDutyCycle(dc)
                  time.sleep(0.01)
            if not os.path.isfile(filename):
                  break # exit while loop

            for dc in range(100, -1, -5):
                  p.ChangeDutyCycle(dc)
                  time.sleep(0.01)
            if not os.path.isfile(filename):
                  break # exit while loop

         p.stop()
         GPIO.cleanup()    
      except KeyboardInterrupt:
         pass
         p.stop()
         GPIO.cleanup()



