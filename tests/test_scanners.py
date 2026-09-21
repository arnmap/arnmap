from unittest.mock import Mock
import pytest
from botocore.exceptions import ClientError
from arnmap import arnmap_helper

def client_error(code):
    return ClientError({"Error": {"Code": code, "Message": "test"}}, "test_operation")

def test_ec2_success():
    client = Mock()
    client.describe_instances.return_value = {"Reservations": [{"Instances": [{"InstanceId": "i-test", "State": {"Name": "running"}}]}]}
    result = arnmap_helper.scan_ec2.__wrapped__(client, "instance", "i-test", "arn:aws:ec2:us-east-1:123456789012:instance/i-test")
    assert result.state == "running"
    assert result.data[0]["describe_instances"]["InstanceId"] == "i-test"

def test_ec2_not_found():
    client = Mock()
    client.describe_instances.side_effect = client_error("InvalidInstanceID.NotFound")
    result = arnmap_helper.scan_ec2.__wrapped__(client, "instance", "i-missing", "arn:aws:ec2:us-east-1:123456789012:instance/i-missing")
    assert result is None

def test_ec2_other_client_error_is_raised():
    client = Mock()
    client.describe_instances.side_effect = client_error("UnauthorizedOperation")
    with pytest.raises(ClientError):
        arnmap_helper.scan_ec2.__wrapped__(client, "instance", "i-test", "arn:aws:ec2:us-east-1:123456789012:instance/i-test")

def test_glue_job_without_runs():
    client = Mock()
    client.get_job.return_value = {"Job": {"Name": "example-job"}}
    client.get_job_runs.return_value = {"JobRuns": []}
    result = arnmap_helper.scan_glue.__wrapped__(client, "job", "example-job", "arn:aws:glue:us-east-1:123456789012:job/example-job")
    assert result.state == "UNKNOWN"
    assert result.data[0]["get_job"]["Name"] == "example-job"

def test_glue_job_with_runs():
    client = Mock()
    client.get_job.return_value = {"Job": {"Name": "example-job"}}
    client.get_job_runs.return_value = {"JobRuns": [{"JobRunState": "SUCCEEDED"}]}
    result = arnmap_helper.scan_glue.__wrapped__(client, "job", "example-job", "arn:aws:glue:us-east-1:123456789012:job/example-job")
    assert result.state == "SUCCEEDED"
