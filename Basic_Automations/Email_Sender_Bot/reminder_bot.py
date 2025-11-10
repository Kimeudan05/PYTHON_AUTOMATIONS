import schedule
import time
from send_email import send_email


def daily_reminder():
    send_email(
        to="savvysolvetech@gmail.com",
        subject="Daily reminder",
        body="This is your daily reminder, make sure to practice and log the results",
    )

    # schedule every day at 9:00 am


schedule.every().day.at("17:10").do(daily_reminder)

print("Schedular running ... press Ctrl+C to stop")
while True:
    schedule.run_pending()
    time.sleep(60)
