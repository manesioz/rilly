from google.cloud import pubsub_v1
from typing import Callable

def create_pubsub_topic(project_id: str, pubsub_topic: str) -> None: 
    '''Method that creates a PubSub Topic in a specified GCP project 
    
    :param project_id: A project_id that is associated with your GCP account
    :type project_id: str 
    
    :param pubsub_topic: The PubSub Topic name 
    :type pubsub_topic: str 
    
    :return: Nothing 
    :rtype: None 
    '''
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=project_id,
      topic=pubsub_topic)
    publisher.create_topic(topic_name) 
    return 
    

def subscribe(project_id: str, pubsub_topic: str, subscription_id: str, wait_time: int, callback: Callable) -> None: 
    '''Method that subscribes to a PubSub Topic and applies callback function to each streamed log
    
    :param project_id: A project_id that is associated with your GCP account
    :type project_id: str
    
    :param pubsub_topic: The PubSub Topic name 
    :type pubsub_topic: str 
    
    :param subscription_id: The Subscription name 
    :type subscription_id: str 
    
    :param wait_time: How long the subscriber should listen for the message (in seconds) 
    :type wait_time: int
    
    :param callback: The callback function that processes the streamed log 
    :type callback: Callable 
    
    :return: Nothing 
    :rtype: None 
    '''
    subscriber = pubsub_v1.SubscriberClient()
    
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=project_id,
      topic=pubsub_topic)
    
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
      project_id=project_id,
      sub=subscription_id)
    
    subscriber.create_subscription(
      name=subscription_name, topic=topic_name)
    
    future = subscriber.subscribe(subscription_name, callback)
    
    try: 
        future.result(timeout=wait_time)
    except KeyboardInterrupt: 
        future.cancel() 
