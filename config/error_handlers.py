import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success':    False,
            'status_code': response.status_code,
            'error':      response.data
        }
        return Response(error_data, status=response.status_code)

    logger.error(
        f"Unhandled exception: {exc}",
        exc_info=True
    )

    return Response({
        'success':    False,
        'status_code': 500,
        'error':      'An unexpected server error occurred. Please try again later.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def handler404(request, exception):
    
    return Response({
        'success':    False,
        'status_code': 404,
        'error':      f"The endpoint '{request.path}' was not found."
    }, status=status.HTTP_404_NOT_FOUND)


def handler500(request):
    
    logger.critical("500 server error occurred")
    return Response({
        'success':    False,
        'status_code': 500,
        'error':      'Internal server error. Our team has been notified.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)