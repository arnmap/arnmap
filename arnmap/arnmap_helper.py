# arnmap_helper.py

import boto3


def scan_dms(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (dms) about the given ARN"""

	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""

	resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	client = session.client('dms')

	if resource_type == "task":

		# Scan 1: describe_replication_tasks
		response_describe_replication_tasks = client.describe_replication_tasks(
			Filters=[
				{
					'Name': 'replication-task-arn',
					'Values': [arn]
				}
			],
			MaxRecords=20
		)

		if not response_describe_replication_tasks:
			return []
		else:
			replication_tasks_dict = response_describe_replication_tasks['ReplicationTasks'][0]
			resource_dict = {'describe_replication_tasks': replication_tasks_dict}
			resource_internal_state = response_describe_replication_tasks['ReplicationTasks'][0]['Status']
			scan_data_list.append(resource_dict)

	else:
		return []

	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]


def scan_ec2(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (ec2) about the given ARN"""

	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""

	resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	client = session.client('ec2')

	if resource_type == "instance":

		# Scan 1: describe_instances
		response_describe_instances = client.describe_instances(
			InstanceIds=[resource_name],
			DryRun=False
		)

		if not response_describe_instances:
			return []
		else:
			instances_dict = response_describe_instances['Reservations'][0]['Instances'][0]
			resource_dict = { 'describe_instances': instances_dict }
			resource_internal_state = response_describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
			scan_data_list.append(resource_dict)

	else:
		return []

	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]

def scan_glue(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (glue) about the given ARN"""
	
	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""

	resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	client = session.client('glue')

	if resource_type == "job":
		
		# Scan 1: get_job_runs (only return most recent job run)
		response_get_job_runs = client.get_job_runs(JobName=resource_name, MaxResults=1)
		
		if not response_get_job_runs:			
			return []			
		else:			
			get_job_runs_dict = response_get_job_runs['JobRuns'][0]
			resource_dict = { 'get_job_runs': get_job_runs_dict }
			resource_internal_state = response_get_job_runs['JobRuns'][0]['JobRunState']
			scan_data_list.append(resource_dict)
				
	elif resource_type == "workflow":
		
		# Scan 1: get_workflow_runs (only return most recent workflow run)
		response_get_workflow_runs = client.get_workflow_runs(Name=resource_name, MaxResults=1, IncludeGraph=False)
		
		if not response_get_workflow_runs:
			return []				
		else:			
			get_workflow_runs_dict = response_get_workflow_runs['Runs'][0]
			resource_dict = { 'get_workflow_runs': get_workflow_runs_dict }
			resource_internal_state = response_get_workflow_runs['Runs'][0]['Status']
			scan_data_list.append(resource_dict)

	else:
		return []
	
	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]


def scan_lambda(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (lambda) about the given ARN"""

	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""

	resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	client = session.client('lambda')

	if resource_type == "function":

		# Scan 1: get_function
		response_get_function = client.get_function(FunctionName=arn, Qualifier='$LATEST')

		if not response_get_function:
			return []
		else:
			configuration_dict = response_get_function
			resource_dict = {'get_function': configuration_dict}
			resource_internal_state = response_get_function['Configuration']['LastUpdateStatus']
			scan_data_list.append(resource_dict)

	else:
		return []

	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]


def scan_redshift(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (redshift) about the given ARN"""

	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""

	resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	client = session.client('redshift')

	if resource_type == "cluster":

		# Scan 1: describe_clusters
		response_describe_clusters = client.describe_clusters(ClusterIdentifier=resource_name, MaxRecords=100)

		if not response_describe_clusters:
			return []
		else:
			clusters_dict = response_describe_clusters['Clusters'][0]
			resource_dict = {'describe_clusters': clusters_dict}
			resource_internal_state = response_describe_clusters['Clusters'][0]['ClusterAvailabilityStatus']
			scan_data_list.append(resource_dict)

	else:
		return []

	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]


def scan_rds(arn, arn_components_list, arn_structure_dict):
	"""Get data from boto3 (rds) about the given ARN"""

	scan_data_list = []
	resource_dict = {}
	resource_internal_state = ""

	resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
	session = boto3.Session(region_name=arn_components_list[arn_structure_dict.get("region")])
	client = session.client('rds')

	if resource_type == "cluster":

		# Scan 1: describe_db_clusters
		response_describe_db_clusters = client.describe_db_clusters(DBClusterIdentifier=resource_name, MaxRecords=100)

		if not response_describe_db_clusters:
			return []
		else:
			db_clusters_dict = response_describe_db_clusters['DBClusters'][0]
			resource_dict = {'describe_db_clusters': db_clusters_dict}
			resource_internal_state = response_describe_db_clusters['DBClusters'][0]['Status']
			scan_data_list.append(resource_dict)

	elif resource_type == "db":

		# Scan 1: describe_db_instances
		response_describe_db_instances = client.describe_db_instances(DBInstanceIdentifier=resource_name, MaxRecords=100)

		if not response_describe_db_instances:
			return []
		else:
			db_instances_dict = response_describe_db_instances['DBInstances'][0]
			resource_dict = {'describe_db_instances': db_instances_dict}
			resource_internal_state = response_describe_db_instances['DBInstances'][0]['DBInstanceStatus']
			scan_data_list.append(resource_dict)

	else:
		return []

	# list[list[dict], string]
	return [scan_data_list, resource_internal_state]


def get_resource_structure(arn, arn_components_list, arn_structure_dict):
	"""Get resource_type and resource_name from resource descriptor in the ARN."""

	# prefix:partition:service:region:accountid:resource/resourceid
	if arn.count(":") == 5:

		resource_structure_dict = {
			'type': 0,
			'name': 1
		}

		resource_list = arn_components_list[arn_structure_dict.get("resource")].split("/")
		resource_type = resource_list[resource_structure_dict.get("type")]
		resource_name = resource_list[resource_structure_dict.get("name")]

	# prefix:partition:service:region:accountid:resource:resourceid
	if arn.count(":") == 6:

		resource_type = arn_components_list[arn_structure_dict.get("resource")]
		resource_name = arn_components_list[arn_structure_dict.get("resourceid")]

	return resource_type, resource_name

