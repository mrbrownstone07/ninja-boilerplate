import uuid
import logging
import threading

# Thread-local storage to store the request ID
_request_id_storage = threading.local()

def get_request_id():
    """Get the current request ID from thread-local storage."""
    return getattr(_request_id_storage, 'request_id', None)

class RequestIDFilter(logging.Filter):
    """Request ID filter to add unique request id to each request log"""
    def filter(self, record):
        # Attach the request ID to the log record
        record.request_id = get_request_id() or "N/A"
        return True

class RequestIDMiddleware:
    """Request ID middleware: Generates unique request ID for each request"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate a unique request ID and attach it to thread-local storage
        request_id = str(uuid.uuid4())[:8]
        _request_id_storage.request_id = request_id
        request.request_id = request_id
        # Continue processing the request
        response = self.get_response(request)

        # Optionally add the request ID to the response headers
        response['X-Request-ID'] = request_id

        return response