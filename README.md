# equicopy

https://equicopy.herokuapp.com/
## Local Dev environment setup:

```
In equicopy/settings.py set DEBUG = True
Activate a virtual environment
Start redis-server
pip install -r requirements.txt
npm install
python manage.py runserver
npm run serve
Go to http://localhost:8080
```

To [start the scheduler](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#starting-the-scheduler)
Run (in 2 separate terminals):
```
celery -A equicopy beat -s <PATH>/celerybeat-schedule
celery -A equicopy worker -l INFO
```
___

Note: The `dist` directory gets installed after the `npm install` command is run.
This is required only for the production version and to use it run:

```
python manage.py collectstatic
gunicorn equicopy.wsgi
Go to http://127.0.0.1:8000
```
___

## Deploy on Heroku:

Update the URLs present in `src/App.vue` to `https://equicopy.herokuapp.com/...`
And also update the credentials in `server/utils/redis.py`

And instead of using celery beat the `Heroku Scheduler` add-on is installed.
Then push to heroku or use `heroku local web` to test first.
___

## Searching:
<details>
<summary>Click Here (Also can be found in the Help button)</summary>
<br>

The `SC_NAME` queries value should always be in Upper Case.
Append a `*` to the string to perform prefix based search.
Else the string has to ben an exact match.
`MIN_PREFIX_LENGTH` has been set to 2 (default).

You can perform the `SC_NAME` query according to the following rules: 
https://oss.redislabs.com/redisearch/Query_Syntax/


To add Numeric filters, seperate the queries with a `&`.
And the value string containing `,` should have no spaces.
Decimal values are also allowed.

Possible Numeric filters include:
`[
    'OPEN',
    'HIGH',
    'LOW',
    'CLOSE',
    'LAST',
    'PREVCLOSE',
    'NO_TRADES',
    'NO_OF_SHRS',
    'NET_TURNOV',
]`


### Example Query:
`SC_NAME: CRES* & OPEN: 0.23,78.6 & LAST: 22.1,40`
</details>
