# arnmap_helper.py

from dataclasses import dataclass
from functools import wraps
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass
class ScanResult:
	data: List[Dict[str, Any]]
	state: Optional[str]


def scanner_aws(service_name):
	"""Decorator to handle generic client setup and error handling."""

	def decorator_scanner(scanner_func):

		@wraps(scanner_func)
		def wrapper_scanner(arn, arn_components_list, arn_structure_dict):

			resource_type, resource_name = get_resource_structure(arn, arn_components_list, arn_structure_dict)
			region = arn_components_list[arn_structure_dict.get("region")]

			try:

				session = boto3.Session(region_name=region)
				client = session.client(service_name)
				return scanner_func(client, resource_type, resource_name, arn)

			except ClientError as e:

				error_code = e.response.get('Error', {}).get('Code', '')

				# if 'NotFound' in error_code or 'NoSuch' in error_code:
				if any(error in error_code for error in ['NotFound', 'NoSuch', 'AccessDenied']):
					return [], ""
				raise e

		return wrapper_scanner

	return decorator_scanner


@scanner_aws('dms')
def scan_dms(client, resource_type, resource_name, arn):
	"""Get data from boto3 (dms) about the given ARN"""

	scan_data_list = []

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
			return None
		else:
			replication_tasks_dict = response_describe_replication_tasks['ReplicationTasks'][0]
			scan_data_list.append({
				'describe_replication_tasks': replication_tasks_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_describe_replication_tasks['ReplicationTasks'][0]['Status']
		)

	else:
		return None


@scanner_aws('ec2')
def scan_ec2(client, resource_type, resource_name, arn):
	"""Get data from boto3 (ec2) about the given ARN"""

	scan_data_list = []

	if resource_type == "instance":

		# Scan 1: describe_instances
		response_describe_instances = client.describe_instances(
			InstanceIds=[resource_name],
			DryRun=False
		)

		if not response_describe_instances:
			return None
		else:
			instances_dict = response_describe_instances['Reservations'][0]['Instances'][0]
			scan_data_list.append({
				'describe_instances': instances_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=instances_dict['State']['Name']
		)

	else:
		return None


@scanner_aws('glue')
def scan_glue(client, resource_type, resource_name, arn):
	"""Get data from boto3 (glue) about the given ARN"""

	scan_data_list = []

	if resource_type == "job":

		# Scan 1: get_job_runs (only return most recent job run)
		response_get_job_runs = client.get_job_runs(JobName=resource_name, MaxResults=1)

		if not response_get_job_runs:
			return None
		else:
			get_job_runs_dict = response_get_job_runs['JobRuns'][0]

			scan_data_list.append({
				'get_job_runs': get_job_runs_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_get_job_runs['JobRuns'][0]['JobRunState']
		)

	elif resource_type == "workflow":

		# Scan 1: get_workflow_runs (only return most recent workflow run)
		response_get_workflow_runs = client.get_workflow_runs(Name=resource_name, MaxResults=1, IncludeGraph=False)

		if not response_get_workflow_runs:
			return None
		else:
			get_workflow_runs_dict = response_get_workflow_runs['Runs'][0]

			scan_data_list.append({
				'get_workflow_runs': get_workflow_runs_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_get_workflow_runs['Runs'][0]['Status']
		)

	else:
		return None


@scanner_aws('lambda')
def scan_lambda(client, resource_type, resource_name, arn):
	"""Get data from boto3 (lambda) about the given ARN"""

	scan_data_list = []

	if resource_type == "function":

		# Scan 1: get_function
		response_get_function = client.get_function(FunctionName=arn, Qualifier='$LATEST')

		if not response_get_function:
			return None
		else:
			configuration_dict = response_get_function

			scan_data_list.append({
				'get_function': configuration_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_get_function['Configuration']['LastUpdateStatus']
		)

	else:
		return None


@scanner_aws('rds')
def scan_rds(client, resource_type, resource_name, arn):
	"""Get data from boto3 (rds) about the given ARN"""

	scan_data_list = []

	if resource_type == "cluster":

		# Scan 1: describe_db_clusters
		response_describe_db_clusters = client.describe_db_clusters(DBClusterIdentifier=resource_name, MaxRecords=100)

		if not response_describe_db_clusters:
			return None
		else:
			db_clusters_dict = response_describe_db_clusters['DBClusters'][0]

			scan_data_list.append({
				'describe_db_clusters': db_clusters_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_describe_db_clusters['DBClusters'][0]['Status']
		)

	elif resource_type == "db":

		# Scan 1: describe_db_instances
		response_describe_db_instances = client.describe_db_instances(DBInstanceIdentifier=resource_name, MaxRecords=100)

		if not response_describe_db_instances:
			return None
		else:
			db_instances_dict = response_describe_db_instances['DBInstances'][0]

			scan_data_list.append({
				'describe_db_instances': db_instances_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_describe_db_instances['DBInstances'][0]['DBInstanceStatus']
		)

	else:
		return None


@scanner_aws('redshift')
def scan_redshift(client, resource_type, resource_name, arn):
	"""Get data from boto3 (redshift) about the given ARN"""

	scan_data_list = []

	if resource_type == "cluster":

		# Scan 1: describe_clusters
		response_describe_clusters = client.describe_clusters(ClusterIdentifier=resource_name, MaxRecords=100)

		if not response_describe_clusters:
			return None
		else:
			clusters_dict = response_describe_clusters['Clusters'][0]

			scan_data_list.append({
				'describe_clusters': clusters_dict
			})

		return ScanResult(
			data=scan_data_list,
			state=response_describe_clusters['Clusters'][0]['ClusterAvailabilityStatus']
		)

	else:
		return None


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

