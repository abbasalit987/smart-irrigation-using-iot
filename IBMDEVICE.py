import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
import urllib.request, json

#Provide your IBM Watson Device Credentials
organization = "9xixnq"
deviceType = "smart-irrigation"
deviceId = "2580"
authMethod = "token"
authToken = "6363822795"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='motoron':
                print("motor is on")
        elif i=='lightoff':
                print("motor is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................

except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
count =3
while True:

        with urllib.request.urlopen("https://node-red-app-20210404114828481.mybluemix.net/data") as url:
            data = json.loads(url.read().decode())
            print(data)

        #print (data)
        def myOnPublishCallback():
            print (data)

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)

        deviceCli.commandCallback = myCommandCallback
        if (count >0):
            if (data['humidity'] < 60):
                url = "https://www.fast2sms.com/dev/bulkV2"

                querystring = {"authorization":"mxb7sZUeQtgdvIJfY6TDVr450ypkuPSG8q92OBERhANCo1KWjllV1kYzEZSiBAt9UGpJ2er6gHFRhTCf","message":"Moisture content is low!","language":"english","route":"q","numbers":"6363822795"}

                headers = {
                'cache-control': "no-cache"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                print(response.text)
                count-=1


# Disconnect the device and application from the cloud
deviceCli.disconnect()
