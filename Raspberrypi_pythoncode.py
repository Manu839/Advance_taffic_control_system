import RPi.GPIO as GPIO
import time
import threading
import requests
# Your ThingSpeak API key and URL
sensor1=15
sensor2=16
sensor3=22
led1=13
led2=11
led3=18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor1,GPIO.IN)
GPIO.setup(sensor2,GPIO.IN)
GPIO.setup(sensor3,GPIO.IN)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
lane1=0
lane2=0
lane3=0
def set(a):
   if(a>3):
      a=3
def sensor1call():
    global lane1
    global objcnt1
    objcnt1=0
    prev=0
    while(True):
       curr=GPIO.input(sensor1)
       if curr!=prev: 
         if curr==1:
          objcnt1+=1
         prev=curr
       lane1=objcnt1
       time.sleep(0.01)
def sensor2call():
    global lane2
    global objcnt2
    objcnt2=0
    prev=0
    while(True):
       curr=GPIO.input(sensor2)
       if curr!=prev: 
         if curr==1:
          objcnt2+=1
         prev=curr
       lane2=objcnt2
       time.sleep(0.01)
def sensor3call():
    global lane3
    global objcnt3
    objcnt3=0
    prev=0
    while(True):
       curr=GPIO.input(sensor3)
       if curr!=prev: 
         if curr==1:
          objcnt3+=1
         prev=curr
       lane3=objcnt3
       time.sleep(0.01)
t1=threading.Thread(target=sensor1call)
t2=threading.Thread(target=sensor2call)
t3=threading.Thread(target=sensor3call)
density1=1
density2=1
density3=1
t1.start()
t2.start()
t3.start()
try:
    while True:
    
# Your ThingSpeak API key and URL
       WRITE_API_KEY = 'BGU9UVNUFHOJR7B2'
       WRITE_API_URL = f'https://api.thingspeak.com/update?api_key={WRITE_API_KEY}'
# The data you want to send to ThingSpeak
# Send the data to ThingSpeak
       field1 = density1
       field2 = density2
       field3 = density3
       data = {'field1': field1, 'field2': field2, 'field3': field3}
       response = requests.post(WRITE_API_URL, data=data)

# Check if the data was successfully sent
       if response.ok:
         print(f'Data sent to ThingSpeak: field1={field1}, field2={field2}, field3={field3}')
       else:
         print(f'Failed to send data to ThingSpeak: {response.text}')
       #setting value for density fo each lane
       objcnt1=0
       objcnt2=0
       objcnt3=0
       print(lane1,lane2,lane3)
       minval=min(min(density1,density2),density3)
       if minval==0:
           minval=1
       if density1==0:
          density1=1
       if density2==0:
          density2=1
       if density3==0:
          density3=1
       density3=density3/minval
       density2=density2/minval
       density1=density1/minval
       set(density1)
       set(density2)
       set(density3)
       timeal=6
    #coverting density into time for each lane
       time1=(density1//1)*timeal
       time2=(density2//1)*timeal
       time3=(density3//1)*timeal
    #turning light on/off on the basis of data given
      #light for lane 1
       GPIO.output(led1,True)
       time.sleep(time1)
       GPIO.output(led1,False)
      #light for lane 2
       GPIO.output(led2,True)
       time.sleep(time2)
       GPIO.output(led2,False)
      #light for lane 3
       GPIO.output(led3,True)
       time.sleep(time3)
       GPIO.output(led3,False)
#time to process data taken by ir sensor till this point
       print("done1")
      #processing for lane 1
      
      #processing for lane 2
      
      #processing for lane 3
      
      #setting density after processing data
       
       
       density1=lane1
       density2=lane2
       density3=lane3

       
except KeyboardInterrupt:
    GPIO.cleanup()
    
