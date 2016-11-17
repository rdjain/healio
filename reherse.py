import serial
import numpy as np
from biosppy.signals import ecg
from twilio.rest import TwilioRestClient
import sys
import pymongo
import heartbeat as hb
#mail=input("Enter the E-Mail Id:") #not input by user incase of standalone
#name=input("Enter your Username:") #not input by user incase of standalone
accsid="AC958bae6ed92bd4227959e70e75b46426" #twilio account
token="06807feb33f0ae36ed87d586e76a79db"    #twilio account
client=TwilioRestClient(accsid,token)
arddata=serial.Serial('/dev/ttyACM0',19200)
while (1==1):
    if(arddata.inWaiting()>0):
        data=arddata.readline()
        if(data[0]=='e'):
            data = data[1:len(data)]
            f=open("ecg.csv", "rw+")
            f.write(str(data)+"\n")
            #print ("ECG value "+data)
        else if(data[0]=='t'):
            #print("Temperature value: "+data)
            temp=int(data)
            f.close()
            dataset = hb.get_data("ecg.csv")
            hb.process(dataset, 0.75, 100)
            bpm = hb.measures['bpm']
            if(temp>37 or bpm>120):
                if(temp>37):
                    message = client.messages.create(to="+919743451835", from_="9097265085",
                                                       body="The temperature is "+temp)
                else if(bpm>120):
                    message = client.messages.create(to="+919743451835", from_="9097265085",
                                                       body="The heart rate is "+bpm +"BPM")
                    
            break   #goto as another option

__author__ = 'mongolab'

SEED_DATA = [
    {
        'email': mail,
        'name': name,
        'bodytemp': temp,
        'hr': bpm
    }            
]           
                
MONGODB_URI = 'mongodb://heal_io_user3:rishabh@ds019926.mlab.com:19926/heal_iomongodb://user:pass@host:port/db' 

def main(args):

    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()       
    vitals = db['vitals']
    vitals.insert(SEED_DATA)
    client.close()

if __name__ == '__main__': ##Only close the connection when the app terminates
    main(sys.argv[1:])






















































































