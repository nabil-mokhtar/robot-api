from collections import deque
import pika , json



class TaskShooter(object):
    """store and fire group of actions when needed"""

    # def __init__(self):
    #     # self.tasks = deque()
    #     # self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 15672, '/', pika.PlainCredentials('user', 'password')))
    #     # self.channel = self.connection.channel()
    #     # self.channel.queue_declare(queue='hello')



    def CloseChannel(self):
        self.channel.close()


    def Fire(self,mission):

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/'))
        channel = connection.channel()
        channel.queue_declare(queue='mission')

        channel.basic_publish(exchange='', routing_key='mission', body=json.dumps(mission))
        print(" [x] Sent 'Hello World!'")
        connection.close()

        



    def Critical_msg(self,msg):

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/'))
        channel = connection.channel()
        channel.queue_declare(queue='critical')

        channel.basic_publish(exchange='', routing_key='mission', body=json.dumps(mission))
        print(" [x] Sent 'Hello World!'")
        connection.close()
