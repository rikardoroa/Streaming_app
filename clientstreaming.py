from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import socket
from serverstreaming import server_streaming
import logging

#creating the log file
logging.basicConfig(filename='client.log', format='%(levelname)s:%(message)s', encoding='utf-8', filemode='w',
                    level=logging.DEBUG)


class client_streaming(server_streaming):

    #init variable and configuring spark enviroment
    def __init__(self):
        server_streaming.__init__(self,  server_streaming.query_input)
        self.arg_query = server_streaming.query_input
        self.arg = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session = SparkSession.builder.master("local[*]") \
            .config("spark.streaming.stopGracefullyOnShutdown", "True") \
            .config("spark.sql.shuffle.partitions", 7) \
            .config("spark.executor.memory", "4g") \
            .config("spark.cores.max", "12") \
            .config("spark.driver.cores", "1") \
            .appName("tweetStream").getOrCreate()

    #capturing the query value.
    def get_args(self, *args):
        x = self.arg_query(*args)
        for item in x:
            self.arg = item
        return self.arg

    def get_tweets_stream(self):
        try:
            #capturing the tweets from the socket(port and host)
            #counting the words and creating the dataframe to show results.
            self.session.sparkContext.setLogLevel("ERROR")
            tweets_df = self.session.readStream.format("socket").option("host", "localhost").option("port", "9998").load()
            tweet_words = tweets_df.select(explode(split(tweets_df.value, " ")).alias("word"))
            tweet_counts = tweet_words.groupBy("word").count()
            tweet_counts.createOrReplaceTempView("tweets")
            df = self.session.sql(f"select word,count from tweets where word like '%{self.arg}%' order by count desc ")
            query = df.writeStream.format("console").outputMode("complete").start()
            query.awaitTermination(60)
            #closing the connection after get all the data
            print("-----please write exit to close server connection------")
            self.client_socket.connect(('localhost', 9998))
            msj = input(">")
            self.client_socket.send(msj.encode('utf-8'))
        except Exception:
            logging.error("Some exception occur during the streaming task")
        finally:
            logging.debug("Streaming task was successfully")