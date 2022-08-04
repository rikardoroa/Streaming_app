## MUTT DATA Challenge - STREAMING APP

## Requisitos Previos

* 1 ->  Cuenta developer en Twitter  con las keys y token previamente configuradas

* 2 -> para esta app solo utilizo el **bearer token** , pero se recomienda utilizar todas las keys

## Instalacion del Container

* 1 -> utilizar el comando **_docker build -it staapp ._** y  **_docker run --rm -it  stapp**   para generar el build y correr el docker container
 

## consideraciones previas
 * 1 - > se generaron las configuraciones mas importantes para el entorno de spark: memoria, particiones y cores de spark.
 

 * 2 -> Se puede especificar la ip del master o setear a traves de la convencion  **local**

 * 3 -> **la app recibe por el momento un solo query**, es decir recibe una palabra, ejemplo:**#halolegends o #gearsofwar o #snydercut o superman** , haciendo el conteo de las demas palabras


## descripcion de los archivos

* 1 -> **serverstreaming**: archivo que genera los tweets a partir de un query, se implemento la funcion **search_recent_tweets** pero tambien se puede implementar la funcion **search_all_tweets** , documentacion adicional aca : https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_all_tweets, adicional se utiliza un socket(puerto y host) para enviar y recibir la informacion de los tweets para realizar el streaming

* 2 -> **clientstreaming**:  archivo que "escucha" o recibe los datos del socket(host y puerto) y realiza el conteo de palabras del tweet enviado, aqui se realiza toda la configuracion de spark:memoria,cores y particiones.

* 3 -> **main**: archivo que ejecuta todo el entorno de la app.


## enjoy!
