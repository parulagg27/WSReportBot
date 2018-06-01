from src.utils.backend import generate_daily_report
from src.utils.login import login
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
print("Starting schedulers")

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21)
def scheduled_job():
    # headers = login('mehul','mehul@hasura') 
    headers = login('parul','parul@hasura')
    generate_daily_report(headers)
    print('This job is run every day at 9pm.')
sched.start()
