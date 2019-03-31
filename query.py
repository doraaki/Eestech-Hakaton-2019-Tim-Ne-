from azure import *
from azure.storage.table.tableservice import TableService
from azure.storage.table.models import Entity
from matplotlib import pyplot as plt
import datetime
import time
import numpy as np

table_service = TableService(account_name='csb61e6613152abx4a5dxbd0',account_key='glQnTM179qQcEckkbAgOBw6PmcMrFA/BkqoOu7g2RS2TilooNHHOnLP3rpIWtJpzd8YbS37+KX4rdTJIIkoxWg==')

#OVAKAV JE FORMAT 2019-03-30T18:48:20.0215023Z

def get_value(measure):

    current_time = str((datetime.datetime.now()).date()) + 'T' + str((datetime.datetime.now() - datetime.timedelta(hours=2) - datetime.timedelta(seconds=5)).time()) + '0Z'
    query_filter = "PartitionKey gt " + '\'' + current_time + '\''

    entities=table_service.query_entities('data', filter=query_filter, num_results=1)
    for entity in entities:
        if(measure == "press"):
            return (entity.Timestamp, entity.pressure)
        if(measure == "temp"):
            return (entity.Timestamp, entity.temperature)
        else:
            return None

def make_graph(measure):

    if(measure != 'press' and measure != 'temp'):
        return None

    current_time = str((datetime.datetime.now()).date()) + 'T' + str((datetime.datetime.now() - datetime.timedelta(hours=2) - datetime.timedelta(seconds=100)).time()) + '0Z'
    query_filter = "PartitionKey gt " + '\'' + current_time + '\''

    entities=table_service.query_entities('data', filter=query_filter, num_results=100)
    Tmps = []
    Timestamps = []
    Pressures = []
    for entity in entities:
        if(measure == 'press'):
            Pressures.append(entity.pressure)
        Timestamps.append(entity.Timestamp)
        if(measure == 'temp'):
            Tmps.append(entity.temperature)

    if(measure == 'press'):
        plt.plot(Timestamps,Pressures)
        plt.savefig('static/press.png')
    if(measure == 'temp'):
        plt.plot(Timestamps,Tmps)
        plt.savefig('static/temp.png')

def get_graph(measure):
    if(measure != 'press' and measure != 'temp'):
        return None

    current_time = str((datetime.datetime.now()).date()) + 'T' + str((datetime.datetime.now() - datetime.timedelta(hours=2) - datetime.timedelta(seconds=100)).time()) + '0Z'
    query_filter = "PartitionKey gt " + '\'' + current_time + '\''

    entities = table_service.query_entities('data', filter=query_filter, num_results=100)
    Tmps = []
    Timestamps = []
    Pressures = []
    for entity in entities:
        if (measure == 'press'):
            Pressures.append(entity.pressure)
        Timestamps.append(entity.Timestamp)
        if (measure == 'temp'):
            Tmps.append(entity.temperature)
    
    if(measure == 'press'):
        return (Timestamps, Pressures)
    if(measure == 'temp'):
        return (Timestamps,Tmps)