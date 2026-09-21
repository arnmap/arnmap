```text
 _______  ______ __   _ _______ _______  _____
 |_____| |_____/ | \  | |  |  | |_____| |_____]
 |     | |    \_ |  \_| |  |  | |     | |
```

# arnmap

`arnmap` is a Python utility for identifying AWS resources from Amazon Resource Names (ARNs).

It parses an AWS ARN, determines the resource type, and uses the appropriate AWS API to inspect the resource.

The project distinguishes between:

- resources that are successfully found
- resources that are confirmed not to exist
- unexpected AWS/API errors

A confirmed missing resource is reported as `NOT_FOUND`; other AWS failures remain `UNKNOWN` rather than being incorrectly reported as missing.

## Usage

### Run as a package module

```bash
python -m arnmap.arnmap --arn "arn:aws:ec2:us-east-1:123456789012:instance/i-example"
```

The module accepts one or more ARNs:

```bash
python -m arnmap.arnmap --arn "arn1" "arn2" "arn3"
```

### Run using the wrapper program

```bash
python arnmap-exec.py --arn "arn:aws:ec2:us-east-1:123456789012:instance/i-example"
```

The wrapper also accepts multiple ARNs:

```bash
python arnmap-exec.py --arn "arn1" "arn2"
```

## Requirements

- Python 3.10+
- AWS credentials configured through the AWS CLI or another supported AWS credential provider
- AWS permissions appropriate for the resources being scanned

Python 3.12 is recommended for production unless the deployment platform dictates otherwise.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/arnmap/arnmap.git
cd arnmap
```

Create the project's virtual environment named `arnmap`:

```bash
python3 -m venv arnmap
source arnmap/bin/activate
```

Install production dependencies:

```bash
pip install -r requirements.txt
```

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## Project Structure

```text
arnmap/
├── arnmap/
│   ├── __init__.py
│   ├── arnmap.py
│   └── arnmap_helper.py
│
├── scripts/
│   └── run_aws_integration_tests.sh
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_arn_validation.py
│   ├── test_arnmap_scan.py
│   ├── test_scanners.py
│   └── integration/
│       ├── __init__.py
│       ├── conftest.py
│       ├── README.md
│       ├── test_dms.py
│       ├── test_ec2.py
│       ├── test_glue.py
│       ├── test_lambda.py
│       ├── test_rds.py
│       └── test_redshift.py
│
├── arnmap-exec.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

The outer `arnmap/` directory is the project root. The inner `arnmap/` directory is the Python package.

### Directory overview

| Path | Purpose |
|---|---|
| `arnmap/` | Main Python package and scanning implementation |
| `scripts/` | Developer/CI helper scripts |
| `tests/` | Unit tests and shared pytest configuration |
| `tests/integration/` | Opt-in tests that connect to real AWS resources |
| `arnmap-exec.py` | Command-line wrapper for scanning ARNs |
| `.env.example` | Template for local integration-test configuration |
| `pytest.ini` | Pytest configuration and integration-test marker |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development and testing dependencies |

## AWS Credentials

Do not store AWS access keys or secret keys in the repository.

Use an AWS CLI profile or another standard AWS credential provider.

For example:

```bash
aws configure --profile arnmap-test
```

Verify the selected account:

```bash
aws sts get-caller-identity --profile arnmap-test
```

Then select the profile for the current shell:

```bash
export AWS_PROFILE=arnmap-test
```

AWS credentials should remain in the AWS credential/profile configuration rather than being placed in `.env`.

## Environment Configuration

The repository contains `.env.example` as a template for local integration-test configuration.

Copy it:

```bash
cp .env.example .env
```

Edit the local values:

```bash
nano .env
```

The actual `.env` file is ignored by Git and must not be committed.

Do not put AWS access keys, secret keys, session tokens, passwords, or other credentials in `.env`.

### Loading `.env` on Linux

For shell-compatible `.env` files, you can load the values into the current shell with:

```bash
set -a
source .env
set +a
```

Then verify a non-secret configuration value:

```bash
echo "$ARNMAP_TEST_ACCOUNT_ID"
```

## Testing

The project uses `pytest`.

### Normal test suite

The normal test command runs the unit tests and excludes tests marked `integration`:

```bash
pytest
```

Normal test execution is intended to be safe:

- no AWS credentials are required
- no AWS API calls are made
- no AWS resources are created

The unit tests are located directly under `tests/`:

```text
tests/
├── test_arn_validation.py
├── test_arnmap_scan.py
└── test_scanners.py
```

### AWS integration tests

The AWS integration suite is strictly opt-in.

Integration tests use real AWS APIs against existing AWS resources. They do not create or delete AWS resources.

The integration tests are located under:

```text
tests/integration/
```

You can run them directly with:

```bash
pytest -m integration
```

Or use the project helper script:

```bash
./scripts/run_aws_integration_tests.sh
```

The helper script enables the integration-test environment and invokes:

```bash
pytest -m integration
```

The script accepts additional pytest arguments. For example:

```bash
./scripts/run_aws_integration_tests.sh -v
```

Before running integration tests, configure the required AWS profile and test-resource environment variables.

The integration suite verifies the authenticated AWS account before running resource tests. If the configured profile points to the wrong account, the tests fail rather than continuing against the wrong environment.

## Integration Test Safety

There are two deliberate safeguards:

1. Normal `pytest` execution excludes integration tests.
2. Integration tests require explicit integration-test configuration.

This prevents accidental AWS API calls during normal development.

The integration helper script is intentionally separate from the normal test command so that AWS-connected tests must be explicitly requested.

## Integration Test Resources

The integration tests use existing AWS resources rather than creating temporary resources for each test.

This avoids:

- unexpected AWS costs
- resource cleanup problems
- resource leaks
- slow tests
- flaky provisioning

The resources used by integration tests should be managed separately, for example through Terraform, CloudFormation, or an explicitly maintained test environment.

## IAM Permissions

The scanner requires read-only permissions for the AWS APIs it uses.

The integration suite also performs an AWS STS `GetCallerIdentity` call to verify which AWS account is being used. `GetCallerIdentity` does not require an IAM permission statement.

The production IAM role should be independently reviewed to ensure that it has only the permissions required by the application.

## Supported Error Behavior

The scanner distinguishes between a resource that does not exist and an unexpected AWS failure.

### Resource does not exist

If AWS explicitly confirms that the requested resource does not exist:

```text
NOT_FOUND
```

### Unexpected AWS failure

Other AWS/API failures should not be interpreted as evidence that the resource is missing.

They remain:

```text
UNKNOWN
```

This distinction is important because an authentication failure, permission failure, throttling event, or other AWS error does not mean that the resource does not exist.

## Development

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the normal test suite:

```bash
pytest
```

Run the AWS integration suite explicitly when an appropriately configured AWS test environment is available:

```bash
./scripts/run_aws_integration_tests.sh
```

Before submitting changes, verify that:

- unit tests pass
- integration tests remain explicitly opt-in
- no AWS credentials are committed
- no generated files or virtual environments are committed
- dependency changes are reflected in the appropriate requirements file
- changes to AWS behavior are covered by appropriate tests

## Security

Never commit:

- AWS access keys
- AWS secret keys
- session tokens
- passwords
- API tokens
- private keys
- production `.env` files
- other credentials or secrets

If credentials are accidentally committed, rotate or revoke them immediately.

## License

MIT No Attribution

Copyright (c) 2025 arnmap

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contributing

Contributions should include appropriate unit tests.

Changes affecting AWS behavior should also be validated against the integration test suite where practical.

Keep AWS integration tests read-only and avoid adding tests that create or delete production resources.

## Special Thanks

```text
Inspired by the legendary Nmap from Fyodor (insecure.org). Not affiliated.
```
