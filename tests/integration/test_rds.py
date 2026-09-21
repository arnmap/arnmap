import os, pytest
pytestmark = pytest.mark.integration
def test_rds_cluster(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_RDS_CLUSTER_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
def test_rds_instance(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_RDS_INSTANCE_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
