from unittest.mock import patch
from arnmap.arnmap import ArnMap
from arnmap.arnmap_helper import ScanResult

def test_invalid_arn():
    result = ArnMap().scan("not-an-arn")
    assert result["resource_status"] == "UNKNOWN"
    assert result["resource_internal_state"] == "UNKNOWN"
    assert result["scans"] == []

def test_unsupported_service():
    result = ArnMap().scan("arn:aws:unsupported:us-east-1:123456789012:thing/example")
    assert result["resource_status"] == "UNKNOWN"
    assert "Method does not exist" in result["scanner_status"]

@patch("arnmap.arnmap.arnmap_helper.scan_ec2")
def test_successful_scan(mock_scan):
    mock_scan.return_value = ScanResult([{"describe_instances": {"InstanceId": "i-test"}}], "running")
    result = ArnMap().scan("arn:aws:ec2:us-east-1:123456789012:instance/i-test")
    assert result["resource_status"] == "FOUND [running]"
    assert result["resource_internal_state"] == "running"
    assert result["scanner_status"] == "FINISHED"

@patch("arnmap.arnmap.arnmap_helper.scan_ec2")
def test_resource_not_found(mock_scan):
    mock_scan.return_value = None
    result = ArnMap().scan("arn:aws:ec2:us-east-1:123456789012:instance/i-missing")
    assert result["resource_status"] == "NOT_FOUND"
    assert result["resource_internal_state"] == "UNKNOWN"

@patch("arnmap.arnmap.arnmap_helper.scan_ec2")
def test_unexpected_exception(mock_scan):
    mock_scan.side_effect = RuntimeError("test failure")
    result = ArnMap().scan("arn:aws:ec2:us-east-1:123456789012:instance/i-test")
    assert result["resource_status"] == "UNKNOWN"
    assert "RuntimeError - test failure" in result["scanner_status"]
