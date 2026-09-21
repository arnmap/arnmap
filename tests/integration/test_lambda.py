import os, pytest
pytestmark = pytest.mark.integration
def test_lambda_function(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_LAMBDA_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
