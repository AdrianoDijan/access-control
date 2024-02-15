import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging to output to the console.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the request
        body = await request.body()
        logger.info(f"Request: {request.method} {request.url} Body: {body.decode()} Headers: {request.headers}")

        response = await call_next(request)

        # Capture response body in a non-destructive way
        response_body = [section async for section in response.__dict__['body_iterator']]
        # Reconstruct the original response
        response.__setattr__('body_iterator', _aiter(response_body))

        # Log the response
        response_body = b''.join(response_body)
        logger.info(f"Response status: {response.status_code} Body: {response_body.decode()}")

        return response

# Helper function to reconstruct response body iterator
async def _aiter(iterable):
    for item in iterable:
        yield item
