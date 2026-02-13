import time
from functools import wraps
from requests.exceptions import RequestException
from .logger import logger

def retry_on_failure(retries=3, delay=1, backoff=2):
    """
    Retry decorator for flaky API calls.
    Power nap strategy: wait * backoff ^ attempt
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except RequestException as e:
                    attempt += 1
                    wait_time = delay * (backoff ** (attempt - 1))
                    logger.warning(f"Request failed: {e}. Retrying in {wait_time}s (Attempt {attempt}/{retries})")
                    time.sleep(wait_time)
                    if attempt == retries:
                        logger.error(f"Function {func.__name__} failed after {retries} retries.")
                        raise
        return wrapper
    return decorator
