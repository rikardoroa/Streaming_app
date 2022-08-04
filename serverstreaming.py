import tweepy
import os
from dotenv import load_dotenv
import socket
import threading

#declaring enviroment variables, token, and socket
load_dotenv()
bearer_token = os.getenv('bearer_token')
client = tweepy.Client(bearer_token)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = "exit"


class server_streaming:

    #init variables
    def __init__(self, socket_=server_socket):
        self.payload_data = []
        self.server_socket = socket_
        self.tquery = ""
     
    #capturing the query value
    def query_input(self, *args):
        for item in args:
            self.tquery = item
        return self.tquery

    #searching the tweets with the query value passed
    def filter_tweet(self):
        try:
            #searching recent tweets
            tweets = client.search_recent_tweets(query=self.tquery, tweet_fields=['author_id', 'created_at'],
                                                 max_results=100)
            for tweet in tweets.data:
                print(tweet.text)
                self.payload_data.append(tweet.text)
        except Exception as e:
            print(e)
    
    #passing the payload with tweets info to the socket
    def sending_tweets(self, conn):
        try:
            while 1:
                print("Connected..sending some tweets")
                for i in range(len(self.payload_data)):
                    conn.send(self.payload_data[i].encode('utf-8'))
                break
        except Exception as e:
            print(e)

    #creating the conexion(Port and host), to passing the data to the socket
    #for the server listening
    def server_connection(self):
        try:
            TCP_IP = 'localhost'
            TCP_PORT = 9998
            self.server_socket.bind((TCP_IP, TCP_PORT))
            self.server_socket.listen(5)
            print("Waiting for TCP connection...")
            print(f"Server is listening on.. {TCP_IP}:{TCP_PORT}")
            while 1:
                conn, addr = self.server_socket.accept()
                thread = threading.Thread(target=self.sending_tweets, args=(conn,))
                thread.start()
                msj = conn.recv(1024).decode('utf-8')
                if msj == msg:
                    conn.close()
        except socket.error as e:
            print(f'\n"Disconnected from server!"', e)