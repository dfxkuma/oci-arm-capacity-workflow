import logging
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import workflow


async def job():
    logging.info("JOB이 scheduler에 의해 실행되었습니다.")
    await workflow()


scheduler = AsyncIOScheduler()
scheduler.add_job(job, "interval", minutes=20)

scheduler.start()

asyncio.get_event_loop().run_forever()
