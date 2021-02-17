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
