import pytest
from arnmap.arnmap import ArnMap

@pytest.fixture
def scanner():
    return ArnMap()

def test_valid_standard_arn(scanner):
    result = scanner._ArnMap__verify_arn("arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef0")
    assert result["prefix"] == "arn"
    assert result["partition"] == "aws"
    assert result["service"] == "ec2"
    assert result["region"] == "us-east-1"
    assert result["accountid"] == "123456789012"
    assert result["resource"] == "instance/i-0123456789abcdef0"

def test_invalid_prefix(scanner):
    assert scanner._ArnMap__verify_arn("foo:aws:ec2:us-east-1:123456789012:instance/i-test") == {}

def test_invalid_partition(scanner):
    assert scanner._ArnMap__verify_arn("arn:invalid:ec2:us-east-1:123456789012:instance/i-test") == {}

def test_invalid_service(scanner):
    assert scanner._ArnMap__verify_arn("arn:aws:EC2:us-east-1:123456789012:instance/i-test") == {}

def test_invalid_region(scanner):
    assert scanner._ArnMap__verify_arn("arn:aws:ec2:us_east_1:123456789012:instance/i-test") == {}

def test_invalid_account_id(scanner):
    assert scanner._ArnMap__verify_arn("arn:aws:ec2:us-east-1:12345:instance/i-test") == {}

def test_missing_resource(scanner):
    assert scanner._ArnMap__verify_arn("arn:aws:ec2:us-east-1:123456789012:") == {}

def test_regionless_arn(scanner):
    result = scanner._ArnMap__verify_arn("arn:aws:iam::123456789012:role/example-role")
    assert result["region"] == ""
