import schedule
import anilisttracker
import time

schedule.every(10).seconds.do(anilisttracker.trackActivity)

while True:
    schedule.run_pending()
    time.sleep(1)