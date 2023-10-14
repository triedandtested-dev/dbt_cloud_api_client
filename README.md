[![PyPI version](https://badge.fury.io/py/dbt-cloud-api-client.svg)](https://badge.fury.io/py/dbt-cloud-api-client)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/dbt-cloud-api-client)](https://pypi.org/project/dbt-cloud-api-client/)
[![CI](https://github.com/triedandtested-dev/dbt_cloud_api_client/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/triedandtested-dev/dbt_cloud_api_client/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/triedandtested-dev/dbt_cloud_api_client/branch/main/graph/badge.svg?token=DLO47S89XY)](https://codecov.io/gh/triedandtested-dev/dbt_cloud_api_client)

# dbt cloud api client
dbt cloud api client

## Usage:

### Install Client.
```
pip install dbt-cloud-api-client
```
### Example.
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

## Contributing

### Via Container
```
docker-compose run --rm dbt_cloud_api_client
```

### Install tox
```
pip install tox
```
