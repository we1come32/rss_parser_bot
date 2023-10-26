from loguru import logger

logger.add("/logs/logs_{time:YYYY-MM-DD}.log",
           level="DEBUG", rotation="10MB", compression="zip")
