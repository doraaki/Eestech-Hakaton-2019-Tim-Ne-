# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import smbus
from Adafruit_BMP085 import BMP085
import smtplib

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=NES.azure-devices.net;DeviceId=Laptop;SharedAccessKey=uP80i5PFlMRG68mL2PTyYh0rWHsbxB3cQe7WghGtpsI="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
default_sleep = 1
less_sleep = 0.5
sleep = default_sleep

# Define the JSON message to send to IoT Hub.
MSG_TXT = "{\"temperature\": %.2f,\"pressure\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def send_email():

    gmail_user = 'ema.p25@gmail.com'
    gmail_password = 'vec132525'

    sent_from = gmail_user
    to = ['nikolaaleksic44@gmail.com']
    subject = 'Raspberry Too Hot!'
    body = 'Temperature over 30C !'

    email_text = """Subject: %s\n

    %s
    """ % (subject, body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        # ...send emails
        server.sendmail(sent_from, to, email_text)
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong...'

def iothub_client_telemetry_sample_run():

    bmp = BMP085(0x77)

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with telemetry values.
            temperature = bmp.readTemperature()
            pressure = bmp.readPressure()
            msg_txt_formatted = MSG_TXT % (temperature, pressure)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if temperature > 30:
              prop_map.add("temperatureAlert", "true")
              if sleep_time == default_sleep:
                send_email()
              sleep_time = less_sleep
            else:
              prop_map.add("temperatureAlert", "false")
              sleep_time = default_sleep

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(sleep_time)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
