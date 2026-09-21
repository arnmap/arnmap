import os, pytest
pytestmark = pytest.mark.integration
def test_redshift_cluster(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_REDSHIFT_CLUSTER_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
