# arnmap_helper.py

import boto3

def scan_glue(arn, arn_list):
	"""Get data from boto3 (glue) about the given ARN"""
	
	resource_list = arn_list[5].split("/")
	resource_type = resource_list[0]
	resource_name = resource_list[1]
	
	session = boto3.Session(region_name=arn_list[3])
	
	client = session.client('glue')
	
	if resource_type == "job":
		
		response_get_job_runs = client.get_job_runs(JobName=resource_name, MaxResults=1)
		
		if not response_get_job_runs:
			
			return []
			
		else:
			
			resource_dict = response_get_job_runs['JobRuns'][0]
			resource_internal_state = response_get_job_runs['JobRuns'][0]['JobRunState']
				
	elif resource_type == "workflow":
		
		response_get_workflow_runs = client.get_workflow_runs(Name=resource_name, MaxResults=1, IncludeGraph=False)
		
		if not response_get_workflow_runs:
			
			return []
				
		else:
			
			resource_dict = response_get_workflow_runs['Runs'][0]
			resource_internal_state = response_get_workflow_runs['Runs'][0]['Status']
			
	session.close()
	
	return [resource_dict, resource_internal_state]
