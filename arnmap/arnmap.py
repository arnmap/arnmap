# arnmap.py

from . import arnmap_helper

import re


class ArnMap:

	def __init__(self):
		
		self.arn_structure_dict = {
			'prefix': 0,
			'partition': 1,
			'service': 2,
			'region': 3,
			'accountid': 4,
			'resource': 5,
			'resourceid': 6
		}

	def scan(self, arn):
		"""Get data from boto3 about the given ARN."""

		scans_list = []
		resource_internal_state = ""
		resource_status = ""
		scan_output_dict = {}

		arn_components_dict = self.__verify_arn(arn)

		if not arn_components_dict:
			return {
				'arn': arn,
				'resource_status': 'UNKNOWN',
				'resource_internal_state': 'UNKNOWN',
				'scans': scans_list,
				'scanner_status': str(
					"ERROR: Unable to verify ARN format."
				)
			}

		method_name = (
			"scan_"
			+ str(arn_components_dict["service"])
		)

		try:

			if hasattr(arnmap_helper, method_name) and callable(getattr(arnmap_helper, method_name)):

				scan_result = getattr(arnmap_helper, method_name)(arn, arn_components_dict)

				if scan_result is None:

					resource_status = "NOT_FOUND"
					resource_internal_state = "NOT_FOUND"

				else:

					scans_list = scan_result.data
					resource_internal_state = scan_result.state

					if not resource_internal_state:

						resource_status = "FOUND"

					else:

						resource_status = (
							"FOUND ["
							+ resource_internal_state
							+ "]"
						)

				scan_output_dict = {
					'arn': arn,
					'resource_status': resource_status,
					'resource_internal_state': resource_internal_state,
					'scans': scans_list,
					'scanner_status': 'FINISHED'
				}

			else:

				scan_output_dict = {
					'arn': arn,
					'resource_status': 'UNKNOWN',
					'resource_internal_state': 'UNKNOWN',
					'scans': scans_list,
					'scanner_status': str(
						"ERROR: Method does not exist in helper module or is not callable ("
						+ method_name
						+ ")"
					)
				}
			
		except Exception as e:

			scan_output_dict = {
				'arn': arn,
				'resource_status': 'UNKNOWN',
				'resource_internal_state': 'UNKNOWN',
				'scans': scans_list,
				'scanner_status': str(
					"Exception: "
					+ type(e).__name__
					+ " - "
					+ str(e)
				)
			}
			
		return scan_output_dict

	def __verify_arn(self, arn):
		"""Confirm that arn is correct format and return a parsed dict of elements."""

		if not isinstance(arn, str):
			return {}

		components_list = arn.split(":")

		if len(components_list) < 6:
			return {}

		arn_dict = {
			"prefix": components_list[self.arn_structure_dict["prefix"]],
			"partition": components_list[self.arn_structure_dict["partition"]],
			"service": components_list[self.arn_structure_dict["service"]],
			"region": components_list[self.arn_structure_dict["region"]],
			"accountid": components_list[self.arn_structure_dict["accountid"]],
			"resource": components_list[self.arn_structure_dict["resource"]],
			"resourceid": (
				":".join(components_list[6:])
				if len(components_list) > 6
				else None
			)
		}

		if arn_dict["prefix"] != "arn":
			return {}

		valid_partitions = {
			"aws",
			"aws-cn",
			"aws-us-gov",
			"aws-iso",
			"aws-iso-b"
		}

		if arn_dict["partition"] not in valid_partitions:
			return {}

		if not re.match(r"^[a-z0-9-]+$", arn_dict["service"]):
			return {}

		if arn_dict["region"] and not re.match(r"[a-z0-9-]+$", arn_dict["region"]):
			return {}

		if arn_dict["accountid"] and not re.match(r"^\d{12}$", arn_dict["accountid"]):
			return {}

		if not arn_dict["resource"]:
			return {}

		return arn_dict

		
def __main(args):
	"""Standard main method within the class. Only called when the program is run 
	directly. Allows execution of code related to the class while still being able
	to import the class in other modules without execution of the main method.
	"""

	scanner = ArnMap()
	for arn in args.arn:
		output = scanner.scan(arn)
		print(output)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Scan AWS resources by ARN.')
	parser.add_argument('--arn', nargs='*', help='List of ARN: "arn1" "arn2" ...', default=[], required=True)
	args = parser.parse_args()
	__main(args)		
