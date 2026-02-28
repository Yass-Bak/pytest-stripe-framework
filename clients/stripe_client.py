import requests
import time
from utils.config import Config
from utils.auth import AuthProvider
from utils.logger import logger
from utils.retry import retry_on_failure

class StripeClient:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(AuthProvider.get_auth_headers())

    def _log_request(self, method, url, **kwargs):
        # Redacting sensitive info if needed (e.g. data with card numbers)
        # keeping it simple for now as per instructions
        logger.info(f"REQUEST: {method} {url}")
        if 'data' in kwargs:
             logger.debug(f"BODY: {kwargs['data']}")

    def _log_response(self, response, duration):
        logger.info(f"RESPONSE: {response.status_code} in {duration:.2f}s")
        if not response.ok:
            logger.error(f"ERROR BODY: {response.text}")

    @retry_on_failure(retries=3, delay=1)
    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self._log_request(method, url, **kwargs)
        
        start_time = time.time()
        try:
            response = self.session.request(method, url, timeout=Config.TIMEOUT, **kwargs)
            duration = time.time() - start_time
            self._log_response(response, duration)
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    def get(self, endpoint, params=None, **kwargs):
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint, data=None, **kwargs):
        return self.request("POST", endpoint, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
