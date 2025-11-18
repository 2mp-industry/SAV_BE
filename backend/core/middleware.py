import time
from fastapi import Request
from .logger import api_logger

async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    
    skip_paths = ["/health", "/docs", "/redoc", "/favicon.ico"]
    if any(request.url.path.startswith(path) for path in skip_paths):
        return await call_next(request)
    
    try:
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        
        # Log only significant requests
        if process_time > 0.5 or response.status_code >= 400:
            api_logger.info(
                f"{request.method} {request.url.path}",
                extra={
                    "status_code": response.status_code,
                    "duration": f"{process_time:.3f}s",
                    "method": request.method,
                    "path": request.url.path
                }
            )
        
        return response
        
    except Exception as e:
        process_time = time.perf_counter() - start_time
        api_logger.error(
            f"Request failed: {request.method} {request.url.path}",
            extra={
                "error": str(e),
                "duration": f"{process_time:.3f}s",
                "method": request.method,
                "path": request.url.path
            },
            exc_info=True
        )
        raise