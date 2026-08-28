# arnmap.py

from . import arnmap_helper


class ArnMap:

	def __init__(self):
		
		self.arn_structure_dict = {
			'prefix': 0,
			'partition': 1,
			'service': 2,
			'region': 3,
			'accountid': 4,
			'resource': 5
		}

	def scan(self, arn):
		"""Get data from boto3 about the given ARN."""

		arn_components_list = self.__verify_arn(arn)
		
		method_name = (
			"scan_" 
			+ str(arn_components_list[self.arn_structure_dict.get("service")])
		)
		
		scan_data_str = ""
		scan_output_str = ""
				
		try:
	
			if hasattr(arnmap_helper, method_name) and callable(getattr(arnmap_helper, method_name)):
				
				resource_scan = getattr(arnmap_helper, method_name)(arn, arn_components_list, self.arn_structure_dict)
				
				scan_data_list = resource_scan[0]
				resource_internal_state = resource_scan[1]
				
				if not scan_data_list:
					
					resource_status = "NOT_FOUND"
					
				elif not resource_internal_state:
				
					resource_status = "FOUND"
				
				else:
				
					resource_status = (
						"FOUND [" 
						+ resource_internal_state 
						+ "]"
					)

				for scan_data_dict in scan_data_list:
					scan_data_str += str(scan_data_dict)
					
				scan_output_str = (
					"arn: " 
					+ arn 
					+ "\n" 
					+ "resource_status: " 
					+ resource_status
					+ "\n"
					+ scan_data_str
				)
				
			else:
				
				scan_output_str = (
					"Method does not exist in helper module or is not callable: " 
					+ method_name
				)				
				
			return scan_output_str
			
		except Exception as e:
			
			scan_output_str = (
				"Exception: " 
				+ type(e).__name__ 
				+ " - " 
				+ str(e)
			)
			
			return scan_output_str


	def __verify_arn(self, arn):
		"""Confirm that arn is correct format and return a parsed list of elements."""
								
		if arn.count(":") < 5:
			return []				
		
		components_list = arn.split(":")
		
		if components_list[self.arn_structure_dict.get("prefix")] != "arn" or components_list[self.arn_structure_dict.get("partition")] != "aws":
			return []
			
		return components_list
		
		
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
