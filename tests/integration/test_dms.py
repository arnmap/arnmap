import os, pytest
pytestmark = pytest.mark.integration
def test_dms_task(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_DMS_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
