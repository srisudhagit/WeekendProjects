from fastapi import FastAPI, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from redis import Redis
from redis_client import create_redis_client
from ratelimiters.FixedWindowRateLimiter import RateLimitMiddleware
from RateLimitConfig import RateLimitConfig

app = FastAPI() 
app.add_middleware(RateLimitMiddleware)

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# create a Redis client instance
redis_client:Redis = create_redis_client()

#dependency injection
def get_redis_client() -> Redis:
    """
    Dependency to get the Redis client.
    """
    return redis_client

@app.get("/ping-redis")
def ping_redis(redis: Redis = Depends(get_redis_client)):
    """
    Endpoint to check the connection to Redis.
    """
    try:
        if redis.ping():
            return {"message": "Pong from Redis!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@app.get("/")
def read_root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/config/{user_id}")
def get_user_config(user_id: str):
    """
    Endpoint to get user configuration from Redis.
    """
    # gets the user configuration from Redis which was set using HMSET config:192.168.1.100 limit 20 window 60
    config = redis_client.hgetall(f"config:{user_id}")
    #config not found return default config
    if not config:
        return {
                "limit": 10,  # Default limit
                "window": 60,  # Default window in seconds
                "souce": "default"
            }
    return {
        "limit": int(config.get("limit")),  
        "window": int(config.get("window")), 
        "source": "redis"       
    }
    
    
@app.post("/config/{user_id}")
def set_user_config(user_id: str, config: RateLimitConfig):
    """
    Endpoint to set user configuration in Redis.
    """
    redis_client.hset(f"config:{user_id}", mapping={"limit": config.limit, "window": config.window})
    return {
        "message": "User configuration updated successfully.",
        "user_id": user_id,
        "limit": config.limit,
        "window": config.window,
        "source": "redis"
    }
    
@app.get("/dashboard")
def get_dashboard(request: Request, ip: str = "127.0.0.1"):
    config = redis_client.hgetall(f"config:{ip}")
    limit = config.get("limit", 10)
    window = config.get("window", 60)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "ip": ip,
        "limit": int(limit),
        "window": int(window)
    })

@app.post("/dashboard")
def post_dashboard(request: Request, ip: str = "127.0.0.1", limit: int = Form(...), window: int = Form(...)):
    redis_client.hset(f"config:{ip}", mapping={"limit": limit, "window": window})
    return RedirectResponse(f"/dashboard?ip={ip}", status_code=303)
