# ArnMap AWS Integration Tests

These tests are opt-in and call real AWS APIs. Set `ARNMAP_RUN_INTEGRATION=1` plus the AWS/resource ARN environment variables before running.

Run unit tests:
`pytest`

Run integration tests:
`pytest -m integration`
