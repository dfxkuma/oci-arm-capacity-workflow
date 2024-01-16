import logging
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from .main import workflow


async def job():
    logging.info("JOB이 scheduler에 의해 실행되었습니다.")
    await workflow()


scheduler = BackgroundScheduler()
scheduler.add_job(job, "interval", minutes=20)

scheduler.start()

asyncio.get_event_loop().run_forever()
