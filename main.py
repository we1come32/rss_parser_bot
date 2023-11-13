from asyncio import run as run_async, get_running_loop, sleep
from logger import logger


async def main():
    from utils.worker import run
    from utils.chat_worker import dp
    from bot import bot

    background_tasks = set()

    logger.info("Starting tasks")
    loop = get_running_loop()
    for task, name in [(run(), "RSS-parser"), (dp.start_polling(bot), "Telegram bot")]:
        task = loop.create_task(task)
        task.set_name(name)
        logger.info("Task {name} is started", name=task.get_name())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    while background_tasks:
        for task in background_tasks:
            await task
            logger.warning("Task {name} is stopped", name=task.get_name())
        await sleep(1)


if __name__ == '__main__':
    run_async(main())
