#script by rikardoroa
from clientstreaming import client_streaming
from serverstreaming import server_streaming
import threading
import time


def execute():
    server = server_streaming()
    server.query_input(input("write the tweet please:"))
    server.filter_tweet()
    server.server_connection()



def execute_client():
    client = client_streaming()
    client.get_tweets_stream()

#executing the main functions in the server and client class
if __name__ == "__main__":
    thread_one = threading.Thread(target=execute)
    thread_one.start()
    time.sleep(20)
    thread_two = threading.Thread(target=execute_client)
    thread_two.start()
    thread_two.join()
    thread_one.join()
