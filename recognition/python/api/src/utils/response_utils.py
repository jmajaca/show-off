from datetime import datetime


def create_error_response(e: Exception, status: int) -> tuple[dict, int]:
    return {'timestamp': datetime.now(), 'error': str(e)}, status
