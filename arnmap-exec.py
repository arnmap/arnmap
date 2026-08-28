# arnmap-exec.py

from argparse import ArgumentParser
from arnmap import arnmap


def main(args):
    scanner = arnmap()
    for arn in args.arn:
        output = scanner.scan(arn)
        print(output)
    

if __name__ == "__main__":

    parser = ArgumentParser(description='Scan AWS resources by ARN.')
    parser.add_argument('--arn', nargs='*', help='List of ARN: "arn1" "arn2" ...', default=[], required=True)
    args = parser.parse_args()
    main(args)
