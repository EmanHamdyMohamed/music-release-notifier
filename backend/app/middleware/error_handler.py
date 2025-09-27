"""
Error handling middleware and utilities
"""
import traceback
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


def create_error_response(
    message: str,
    status_code: int,
    request: Request,
    error_id: str = None,
    details: Dict[str, Any] = None
) -> JSONResponse:
    """Create a standardized error response"""
    error_data = {
        "error": True,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.utcnow().isoformat(),
        "path": str(request.url)
    }
    
    if error_id:
        error_data["error_id"] = error_id
    
    if details:
        error_data["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content=error_data
    )


def log_error(error: Exception, request: Request, error_id: str = None):
    """Log error with context"""
    if error_id:
        logging.error(f"Error ID: {error_id}")
    
    logging.error(f"Request: {request.method} {request.url}")
    logging.error(f"Error: {str(error)}")
    logging.error(f"Traceback: {traceback.format_exc()}")


class ErrorHandler:
    """Centralized error handling class"""
    
    @staticmethod
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle FastAPI HTTP exceptions"""
        return create_error_response(
            message=exc.detail,
            status_code=exc.status_code,
            request=request
        )
    
    @staticmethod
    async def handle_general_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle general exceptions"""
        error_id = f"ERR_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Log the error
        log_error(exc, request, error_id)
        
        return create_error_response(
            message="Internal server error",
            status_code=500,
            request=request,
            error_id=error_id
        )
    
    @staticmethod
    async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        """Handle ValueError exceptions"""
        return create_error_response(
            message=f"Invalid value: {str(exc)}",
            status_code=400,
            request=request
        )
    
    @staticmethod
    async def handle_connection_error(request: Request, exc: ConnectionError) -> JSONResponse:
        """Handle connection errors"""
        return create_error_response(
            message="Service temporarily unavailable",
            status_code=503,
            request=request
        )
    
    @staticmethod
    async def handle_timeout_error(request: Request, exc: TimeoutError) -> JSONResponse:
        """Handle timeout errors"""
        return create_error_response(
            message="Request timeout",
            status_code=504,
            request=request
        )
