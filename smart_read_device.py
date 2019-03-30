  GNU nano 2.7.4                               File: smart_read_device.py                                         

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
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output$
CONNECTION_STRING = "HostName=NES.azure-devices.net;DeviceId=Laptop;SharedAccessKey=uP80i5PFlMRG68mL2PTyYh0rWHsbx$

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
default_sleep = 1
less_sleep = 0.5
sleep = default_sleep

# Define the JSON message to send to IoT Hub.
MSG_TXT = "{\"average_temperature\": %.2f,\"max_temperature\": %.2f,\"min_temperature\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

CONNECTION_STRING = "HostName=NES.azure-devices.net;DeviceId=Laptop;SharedAccessKey=uP80i5PFlMRG68mL2PTyYh0rWHsbx$

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
default_sleep = 1
less_sleep = 0.5
sleep = default_sleep

# Define the JSON message to send to IoT Hub.
MSG_TXT = "{\"average_temperature\": %.2f,\"max_temperature\": %.2f,\"min_temperature\": %.2f}"

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
    subject = 'Too hot Raspberry'
    body = 'Temperature over 27C !'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()

    gmail_user = 'ema.p25@gmail.com'
    gmail_password = 'vec132525'

    sent_from = gmail_user
    to = ['nikolaaleksic44@gmail.com']
    subject = 'Too hot Raspberry'
    body = 'Temperature over 27C !'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

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

    cnt_of_messages = 0
    average_temperature = 0
    max_temperature = 0
    time_at_max = 0
    min_temperature = 10000
    time_at_min = 0
        server.login(gmail_user, gmail_password)
        # ...send emails
        server.sendmail(sent_from, to, email_text)
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong...'

def iothub_client_telemetry_sample_run():

    bmp = BMP085(0x77)

    cnt_of_messages = 0
    average_temperature = 0
    max_temperature = 0
    time_at_max = 0
    min_temperature = 10000
    time_at_min = 0

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with telemetry values.
            temperature = bmp.readTemperature()
            pressure = bmp.readPressure()
            average_temperature = average_temperature*cnt_of_messages + temperature
            cnt_of_messages += 1
            average_temperature /= cnt_of_messages
            if temperature > max_temperature:
              max_temperature = temperature
            if temperature < min_temperature:
              min_temperature = temperature 
            msg_txt_formatted = MSG_TXT % (average_temperature, max_temperature, min_temperature)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with telemetry values.
            temperature = bmp.readTemperature()
            pressure = bmp.readPressure()
            average_temperature = average_temperature*cnt_of_messages + temperature
            cnt_of_messages += 1
            average_temperature /= cnt_of_messages
            if temperature > max_temperature:
              max_temperature = temperature
            if temperature < min_temperature:
              min_temperature = temperature 
            msg_txt_formatted = MSG_TXT % (average_temperature, max_temperature, min_temperature)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if temperature > 27:
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




