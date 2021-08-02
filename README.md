[![PyPI version](https://badge.fury.io/py/dbt-cloud-api-client.svg)](https://badge.fury.io/py/dbt-cloud-api-client)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/dbt-cloud-api-client)](https://pypi.org/project/dbt-cloud-api-client/)
<!-- [![GitHub Actions (Tests)](https://github.com/ymyzk/tox-gh-actions/workflows/Tests/badge.svg)](https://github.com/ymyzk/tox-gh-actions) -->
<!-- [![codecov](https://codecov.io/gh/ymyzk/tox-gh-actions/branch/master/graph/badge.svg?token=7RWjRk2LkX)](https://codecov.io/gh/ymyzk/tox-gh-actions) -->

# dbt cloud api client
dbt cloud api client

Usage:

## Install Client.
```
pip install dbt-cloud-api-client
```
## Example.
```python
import time

from dbt_cloud_api_client.client import DbtCloudClient
...

client = DbtCloudClient(token='<token>')

account = client.get_account_by_name('<ACCOUNT_NAME>')

job = account.get_job_by_name('<JOB NAME IN DBT CLOUD>')
run = job.run('Job triggered from python.')

while not run.is_finished():
    print('{} - {}'.format(run.id, run.status))
    run.reload()
    # print(run.data) # display all details of run.
    # sleep for a period of time
    time.sleep(60)
print('{} - {}'.format(run.id, run.status))
```

# Contributing

## Install tox
```
pip install tox
```
