# arnmap_helper.py

import boto3


def scan_glue(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (glue) about the given ARN"""
	
	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""
	
	resource_structure_dict = {
		'type': 0,
		'name': 1
	}	
	
	resource_list = arn_components_list[arn_structure_dict.get("resource")].split("/")
	resource_type = resource_list[resource_structure_dict.get("type")]
	resource_name = resource_list[resource_structure_dict.get("name")]
	
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	
	client = session.client('glue')

	print("resource_name: " + resource_name)

	if resource_type == "job":
		
		# Job Scan 1: Only return most recent job run
		response_get_job_runs = client.get_job_runs(JobName=resource_name, MaxResults=1)
		
		if not response_get_job_runs:			
			return []			
		else:			
			get_job_runs_dict = response_get_job_runs['JobRuns'][0]
			resource_dict = { 'get_job_runs': get_job_runs_dict }
			resource_internal_state = response_get_job_runs['JobRuns'][0]['JobRunState']
			scan_data_list.append(resource_dict)
				
	elif resource_type == "workflow":
		
		# Workflow Scan 1: Only return most recent workflow run
		response_get_workflow_runs = client.get_workflow_runs(Name=resource_name, MaxResults=1, IncludeGraph=False)
		
		if not response_get_workflow_runs:
			return []				
		else:			
			get_workflow_runs_dict = response_get_workflow_runs['Runs'][0]
			resource_dict = { 'get_workflow_runs': get_workflow_runs_dict }
			resource_internal_state = response_get_workflow_runs['Runs'][0]['Status']
			scan_data_list.append(resource_dict)
	
	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]
