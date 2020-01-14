from google.cloud import logging_v2
from google.cloud import logging 
from typing import Generator


def list_table_change_logs(project_id: str, dataset_id: str) -> Generator[str, None, None]: 
  '''Helper function that returns all relevant logs (directly from the Stackdriver API, not PubSub)
  
  :param project_id: The project_id that is associated with your GCP account and BigQuery Table
  :type project_id: str 
  
  :param dataset_id: The name of the dataset that you want to track/replicate via CDC
  :type dataset_id: str 
  
  :return: A Generator object representing an iterable of relevant logs
  :rtype: Generator
  '''
  client = logging_v2.LoggingServiceV2Client()
  resource_names = ["projects/{}".format(project_id)]

  #filter logs that reflect a bigquery table insert/update/delete only (for the specified project and dataset)  
  query = '''
  resource.labels.dataset_id="{dataset_id}"
  resource.labels.project_id="{project_id}"
  protoPayload.metadata.@type="type.googleapis.com/google.cloud.audit.BigQueryAuditMetadata"
  (protoPayload.metadata.tableDataChange.deletedRowsCount > "0" OR protoPayload.metadata.tableDataChange.insertedRowsCount > "0")
  '''.format(project_id=project_id, dataset_id=dataset_id) 
  
  for log in client.list_log_entries(resource_names, filter_=query):
      yield log 

      
def create_sink(sink_id: str, project_id: str, dataset_id: str, pubsub_topic: str, query: str = None) -> None:
    """Creates a sink to export logs to the given PubSub Topic.
    
    :param sink_id: A unique identifier for the sink 
    :type sink_id: str 
    
    :param project_id: The project_id that is associated with your GCP account and BigQuery Table
    :type project_id: str
    
    :param pubsub_topic: The PubSub Topic that the logs will export to 
    :type pubsub_topic: str 
    
    :param query: The query that filters what logs will be exported 
    :type query: str 
    
    :return: Nothing
    :rtype: None
    """
    client = logging.Client()    
    destination = 'pubsub.googleapis.com/projects/{project_id}/topics/{pubsub_topic}'.format(
        project_id=project_id, pubsub_topic=pubsub_topic)
    
    if query is None: 
      query = '''
      resource.labels.dataset_id="{dataset_id}"
      resource.labels.project_id="{project_id}"
      protoPayload.metadata.@type="type.googleapis.com/google.cloud.audit.BigQueryAuditMetadata"
      (protoPayload.metadata.tableDataChange.deletedRowsCount > "0" OR protoPayload.metadata.tableDataChange.insertedRowsCount > "0")
      '''.format(project_id=project_id, dataset_id=dataset_id)
      
    sink = client.sink(
        sink_id,
        filter_=query,
        destination=destination)

    if sink.exists():
        print('Sink {} already exists.'.format(sink.name))
        return
    else: 
        sink.create()
        print('Created sink {}'.format(sink.name))
        return 
