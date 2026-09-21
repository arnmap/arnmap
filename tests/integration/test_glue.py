import os, pytest
pytestmark = pytest.mark.integration
def test_glue_job(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_GLUE_JOB_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
def test_glue_workflow(arn_scanner):
    r = arn_scanner.scan(os.environ["ARNMAP_GLUE_WORKFLOW_ARN"])
    assert r["scanner_status"] == "FINISHED"
    assert r["resource_status"].startswith("FOUND")
