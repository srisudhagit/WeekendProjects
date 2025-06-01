from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from redis_client import create_redis_client
from redis import Redis 

DEFAULT_LIMIT = 10
DEFAULT_WINDOW = 60

# create a Redis client instance
redis_client:Redis = create_redis_client()

class RateLimitMiddleware(BaseHTTPMiddleware):
   async def dispatch(self, request, call_next):
       
       #starting rate limit logic
        # step-1 identify the client
        client_ip = request.client.host
        redis_key = f"rate_limit:{client_ip}"
         
        # step-2 check the current request count    
        current_requests = redis_client.get(redis_key)
        if current_requests is None:
            #client doesn't have any requests yet, initialize the count to 1
            # and set the expiration time for the key with the default window
            redis_client.set(redis_key, 1, ex=DEFAULT_WINDOW)  # Set initial request count with expiration
        else:
            current_requests = redis_client.hgetall(f"config:{client_ip}").get("limit", DEFAULT_LIMIT)
            current_requests = int(current_requests)  # Convert to integer
            if current_requests >= DEFAULT_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Try again later."}
                )
            else:
                redis_client.incr(redis_key)
                
        # step-3 process the request
        response = await call_next(request)
        # step-4 return the response
        return response
                
           
    
       