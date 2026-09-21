import os, pytest
pytestmark = pytest.mark.integration
def test_ec2_instance(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_EC2_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
