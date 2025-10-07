# import argparse

from arnmap import arnmap

# DEBUG: list attributes, methods, and classes in module
# print(dir(arnmap))

def main(args):
    print("This is the main entry point of the program.")
    print(f"Arguments: {args}")
	# arnmap = arnmap()
	# output = arnmap.scan("arn:aws:glue:us-east-1:123456789012:job/test")
	# print(output)    
    

if __name__ == "__main__":
    parser = ArgumentParser(description='Scan AWS resources by ARN.')
    # parser.add_argument('--arn', type=str, help='Enter the Amazon Resource Name', required=True)
    parser.add_argument('--arn', nargs='*', help='A list of items.', default=[], required=True)
    args = parser.parse_args()
    main(args)
