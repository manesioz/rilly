from google.cloud import logging_v2
from typing import Generator


def list_table_change_logs(project_id: str, dataset_id: str) -> Generator[str, None, None]: 
  '''
  Helper function that returns all relevant logs (directly from the Stackdriver API, not PubSub)
  
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
