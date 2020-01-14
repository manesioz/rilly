<p align="center">
  Distributed change data capture (CDC) platform for Google BigQuery
  <br><br>
  <img src="https://github.com/manesioz/rilly/blob/master/assets/rilly.png">
</p>

### What is Change Data Capture? 
Change data capture (CDC) is a set of software design patterns used to determine (and track) the data that has changed so that action can be taken using the changed data. Instead of continuously polling a database for changes (which is costly if you do it often and inaccurate if you don't), rilly uses the log-based approach (as does [`debezium`](https://debezium.io) and all other major CDC frameworks). 


### Why `rilly`?
There is currently no CDC plug-in for BigQuery that I am aware of, and certainly none for Python. The goal of this package is to be as simple and non-opinionated as possible to allow developers to have full control over how they want to stream and parse their change events. 


### Installation 

```python
pip install rilly
```

### Authentication 
This library uses Google's PubSub and Stackdriver APIs, so follow the authentication process [here](https://cloud.google.com/pubsub/docs/reference/libraries#setting_up_authentication). 


### Usage 
Say you want to track all update/delete/insert events in your BigQuery dataset. After authenticating the Google Python Client APIs: 

```python
from rilly import logging, stream

stream.create_pubsub_topic('my-project-id', 'pubsub-topic') #create a PubSub topic to send your change events to 
logging.create_sink('sink-id', 'my-project-id', 'my-dataset-id', pubsub_topic='pubsub-topic') #create sink to send logs to PubSub topic

def custom_callback(message: str) -> str: #custom callback function to perform some action on each event
    print('Received message data: {}'.format(message.data))
    return message 
    
#create subscription to PubSub topic, apply custom_callback() to each streamed log
stream.subscribe('my-project-id', 'pubsub-topic', 'cdc-subscription', 30, custom_callback) 
```



