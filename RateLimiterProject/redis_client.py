import os
import sys
from redis import Redis,ConnectionError
from dotenv import load_dotenv
import logging

load_dotenv() # Load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.INFO)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_DB = os.getenv('REDIS_DB', 0)

def create_redis_client() -> Redis:
    """
    Create a Redis client with the specified configuration.
    """
    try:
        redis_client = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
        # Test the connection
        conn_resp = redis_client.ping()
        if not conn_resp:
            raise ConnectionError("Failed to connect to Redis server.")
        # Log the successful connection
        logging.info("Connected to Redis server successfully.")
        return redis_client
    except ConnectionError as e:
        logging.error(f"Could not connect to Redis server: {e}")
        sys.exit(1)  # Exit the program if connection fails

