# dbt cloud api client
dbt cloud api client


## Install tox
```
pip install tox
```


Usage:
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
