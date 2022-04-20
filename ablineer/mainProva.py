from allineerTemplate import *

import pika
import serial
import time

tmpMessage = ""


def getTrackToU():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Esploratore')
    channel.basic_publish(exchange='', routing_key='Esploratore', body='Esplo:u')

    def callback(ch, method, properties, body):
        tmpMessage = body.decode('utf-8')

    channel.basic_consume(callback, queue='Esploratore', no_ack=True)
    channel.start_consuming()
    dire = tmpMessage.decode('utf-8').split(', ')
    return dire


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
explo = connection.channel()

explo.queue_declare(queue='Esploratore')

explo.basic_publish(exchange='',
                    routing_key='hello',
                    body='Hello World!')

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


def getLidar():
    return {}


while True:
    pass

connection.close()
