from loguru import logger

from server import serve

if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        logger.info("^C received, shutting down the server")
    except Exception as e:
        logger.exception(f"Exception occurred: {e}")
