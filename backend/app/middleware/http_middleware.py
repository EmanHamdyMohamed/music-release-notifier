"""
HTTP middleware for request/response processing
"""
from fastapi import Request, HTTPException
from app.middleware.error_handler import ErrorHandler


async def error_handling_middleware(request: Request, call_next):
    """
    Global error handling middleware that catches all unhandled exceptions
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        # Let FastAPI handle HTTP exceptions through exception handlers
        raise
    except Exception as e:
        # Handle unexpected errors through the error handler
        return await ErrorHandler.handle_general_exception(request, e)
