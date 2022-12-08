from apscheduler.schedulers.background import BackgroundScheduler
from sub import returns, delivers, results
import time
import os
from dotenv import load_dotenv

load_dotenv()

RETURNS_INTERVAL=int(os.getenv("RETURNS_INTERVAL"))
DELIVER_INTERVAL=int(os.getenv("DELIVER_INTERVAL"))
RESULTS_INTERVAL=int(os.getenv("RESULTS_INTERVAL"))

scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(returns.app_handler, 'interval', minutes=RETURNS_INTERVAL, id='returns')
scheduler.add_job(delivers.app_handler, 'interval', seconds=DELIVER_INTERVAL, id='delivers')
scheduler.add_job(results.app_handler, 'interval', seconds=RESULTS_INTERVAL, id='results')

count = 0
while True:
  print("Running main process...............")
  time.sleep(1)