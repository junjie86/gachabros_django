# myproject/middleware.py


import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

 
           
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Log request details
        print(f"Request Method: {request.method}")
        print(f"Request Path: {request.path}")
        print(f"User: {request.user}")  # Ensure this is not None

        response = self.get_response(request)
        return response
      
    def process_request(self, request):
        # Log request details
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request Path: {request.path}")
        # logger.info(f"Headers: {dict(request.headers)}")
        
        # Log request body (if applicable)
        try:
            body = request.body.decode('utf-8')
            logger.info(f"Body: {body}")
        except Exception as e:
            logger.info(f"Error decoding body: {e}")

    def process_response(self, request, response):
        # Log response details
        logger.info(f"Response Status Code: {response.status_code}")
        # logger.info(f"Response Content: {response.content.decode('utf-8')}")
        return response