from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from redis_client import create_redis_client
from redis import Redis 
import logging

DEFAULT_LIMIT = 10
DEFAULT_WINDOW = 60

logging.basicConfig(level=logging.INFO)

# create a Redis client instance
redis_client:Redis = create_redis_client()

class RateLimitMiddleware(BaseHTTPMiddleware):
   async def dispatch(self, request, call_next):
       
        logging.info(f"Middleware running") 
        
        # step-1 get client config if available or use default values
        client_ip = request.client.host
        current_config = redis_client.hgetall(f"config:{client_ip}")
        limit = int(current_config.get("limit", DEFAULT_LIMIT))
        window = int(current_config.get("window", DEFAULT_WINDOW))
        
        # step-2 fetch client usage from Redis 
        redis_key = f"rate_limit:{client_ip}"
        current_requests = redis_client.get(redis_key)
        if current_requests is None:
            #client doesn't have any requests yet, initialize the count to 1
            # and set the expiration time for the key with the default window
            redis_client.set(redis_key, 1, ex=DEFAULT_WINDOW) 
        else:
            # client exists so check the limit
            current_requests = int(current_requests)
            if current_requests >= limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Try again later."}
                )
            else:
                # increment the request count for the client
                redis_client.incr(redis_key)
                
        # step-3 process the request
        response = await call_next(request)
        # step-4 return the response
        return response
                
           
    
       