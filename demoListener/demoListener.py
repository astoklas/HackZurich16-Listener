#!/usr/bin/env python
import pika
import os
import time
import json
from influxdb import InfluxDBClient

#
# Write values to the influxdb
# Tags: SensorID
# fields: all types defined in the message from rabbitmq
# measurement is called "HackZurich16" by default
# DB is called "HackZurich16" by default

def writeInflux(db, msg):
    data = msg['data']
    myPoint = []
    myDB = {}
    myTags = {}
    myFields = {}
    myTags['SensorID']=msg['id']
    myTags['type']=msg['type']

    for i in range(0,len(data)):
        if data[i]['type'] == "level":
            field = data[i]['type'] + '_' + str(data[i]['id'])
            myFields[field] = data[i]['value']
        else:
            myFields[data[i]['type']] = data[i]['value']


    myDB['measurement']= db_influxdb
    myDB['tags']=myTags
    myDB['fields']=myFields
    myPoint.append(myDB)
    json_data = json.dumps(myPoint, sort_keys=True, indent=4, separators=(',', ': '))
    #print json_data
    #print " [x] Writing Data to InfluxDB"
    db.write_points(myPoint)
#    return myDB

#
# Reading environment variables for the message queue and influxdb
# HOST_INFLUXDB and HOST_RABBITMQ
# not tested yet
host_rabbit = os.environ.get('RABBITMQ_HOST', "localhost")
user_rabbit = os.environ.get('RABBITMQ_DEFAULT_USER', "cisco")
passwd_rabbit = os.environ.get('RABBITMQ_DEFAULT_PASS', "C1sco123")
queue_rabbit = os.environ.get('RABBITMQ_QUEUE', "HackZurich16")
port_rabbit = int(os.environ.get('RABBITMQ_PORT', "5672"))

host_influxdb = os.environ.get('INFLUXDB_HOST', "localhost")
user_influxdb = os.environ.get('INFLUXDB_DEFAULT_USER', "root")
passwd_influxdb = os.environ.get('INFLUXDB_DEFAULT_PASS', "root")
db_influxdb = os.environ.get('INFLUXDB_NAME', "HackZurich16")
port_influxdb = int(os.environ.get('INFLUXDB_PORT', "8086"))

#
# Connecting to RabbitMQ
# and aquire channel "HackZurich16"
#
credentials = pika.PlainCredentials(user_rabbit, passwd_rabbit)
connection = None
print "Establish Connection to RabbitMQ ....", host_rabbit
while (None == connection):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_rabbit, port=port_rabbit, credentials=credentials))
    except:
        connection = None
        print "Connection to RabbitMQ failed, retry in 5 sec"
        time.sleep(5)
channel = connection.channel()
channel.queue_declare(queue=queue_rabbit)
print "Done"
#
# Connecting to InluxDB
#
print "Establish Connection to influxDB ....", host_influxdb
db = None
while db is None:
    try:
        db = InfluxDBClient(host=host_influxdb,port=port_influxdb,username=user_influxdb,password=passwd_influxdb,database=db_influxdb)
    except:
        db = None
        print "Connection to Influx failed, retry in 5 sec"
        time.sleep(5)
print "Create DB"
time.sleep(1)
db.drop_database(db_influxdb)
db.create_database(db_influxdb)
db.create_retention_policy('awesome_policy', '3d', 3, default=True)

print "Done"
print "Ready to listen ...."
def callback(ch, method, properties, body):
    #print(" [x] Received %r" % body)
    writeInflux(db,json.loads(body))

channel.basic_consume(callback,queue=queue_rabbit,no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
