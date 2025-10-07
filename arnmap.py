# arnmap.py

import arnmap_helper

class arnmap:

	def scan(self, arn):
		"""Get data from boto3 about the given ARN"""
		
		index_resource = 0
		index_internal_state = 1		
		index_resource_type = 2

		arn_list = self._arnmap__verify_arn(arn)
		
		method_name = (
			"scan_" 
			+ str(arn_list[index_resource_type])
		)
		
		scan_output = ""
				
		try:
	
			if hasattr(arnmap_helper, method_name) and callable(getattr(arnmap_helper, method_name)):
				
				resource_scan = getattr(arnmap_helper, method_name)(arn, arn_list)
				resource_dict = resource_scan[index_resource]
				resource_internal_state = resource_scan[index_internal_state]
				
				if not resource_dict:
					
					resource_status = "NOT_FOUND"
					
				elif not resource_internal_state:
				
					resource_status = "FOUND"
				
				else:
				
					resource_status = (
						"FOUND [" 
						+ resource_internal_state 
						+ "]"
					)
								
				scan_output = (
					"arn: " 
					+ arn 
					+ "\n" 
					+ "resource_status: " 
					+ resource_status
					+ "\n"
					+ str(resource_dict)
				)
				
			else:
				
				scan_output = (
					"Method does not exist in arnmap_module.py or is not callable: " 
					+ method_name
				)				
				
			return scan_output
			
		except Exception as e:
			
			scan_output = (
				"Exception: " 
				+ type(e).__name__ 
				+ " - " 
				+ str(e)
			)
			
			return scan_output


	def __verify_arn(self, arn):
		"""Confirm that arn is correct format and return a parsed list of elements"""
		
		index_arn = 0
		index_aws = 1
								
		if arn.count(":") < 5:
			return []				
		
		arn_list = arn.split(":")
		
		if arn_list[index_arn] != "arn" or arn_list[index_aws] != "aws":
			return []
			
		return arn_list
		
		
	def __main(args):
		"""Standard main method within the class. Only called when the program is run 
		directly. Allows execution of code related to the class. While still being able 
		to import the class in other modules without execution of the main method."""
		
		import sys
		if not args.arn:
			sys.exit(1)		
		print("args.arn:", args.arn)
		# Loop through array of arn strings	
			# arnmap = arnmap()
			# output = arnmap.scan("arn:aws:glue:us-east-1:123456789012:job/test")
			# print(output)    
		

	if __name__ == "__main__":
		"""This is the entry point when the program is run directly."""
		
		import argparse
		parser = argparse.ArgumentParser(description='Scan AWS resources by ARN.')
		parser.add_argument('--arn', nargs='*', help='list of Amazon Resource Names: "arn1" "arn2" ...', default=[], required=True)
		args = parser.parse_args()
		__main(args)		
