import os
import boto3
import pytest

@pytest.fixture(scope="session")
def aws_session():
    if os.getenv("ARNMAP_RUN_INTEGRATION") != "1":
        pytest.skip("Set ARNMAP_RUN_INTEGRATION=1 to run AWS integration tests")
    required = ["ARNMAP_AWS_PROFILE", "ARNMAP_AWS_ACCOUNT_ID", "ARNMAP_AWS_REGION"]
    required += ["ARNMAP_DMS_ARN", "ARNMAP_EC2_ARN", "ARNMAP_GLUE_JOB_ARN", "ARNMAP_GLUE_WORKFLOW_ARN",
                 "ARNMAP_LAMBDA_ARN", "ARNMAP_RDS_CLUSTER_ARN", "ARNMAP_RDS_INSTANCE_ARN", "ARNMAP_REDSHIFT_CLUSTER_ARN"]
    missing = [x for x in required if not os.getenv(x)]
    if missing:
        pytest.fail("Missing integration environment variables: " + ", ".join(missing))
    os.environ["AWS_PROFILE"] = os.environ["ARNMAP_AWS_PROFILE"]
    os.environ["AWS_DEFAULT_REGION"] = os.environ["ARNMAP_AWS_REGION"]
    session = boto3.Session(profile_name=os.environ["ARNMAP_AWS_PROFILE"], region_name=os.environ["ARNMAP_AWS_REGION"])
    actual = session.client("sts").get_caller_identity()["Account"]
    if actual != os.environ["ARNMAP_AWS_ACCOUNT_ID"]:
        pytest.fail(f"AWS account mismatch: expected {os.environ['ARNMAP_AWS_ACCOUNT_ID']}, got {actual}")
    return session

@pytest.fixture(scope="session")
def arn_scanner(aws_session):
    from arnmap.arnmap import ArnMap
    return ArnMap()
