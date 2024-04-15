from os import environ

from redis import Redis


redis_host = environ["REDIS_HOST"]
redis_port = environ["REDIS_PORT"]
redis_db = environ["REDIS_DB"]
redis_password = environ.get("REDIS_PASSWORD", None)

redis_client = Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password, decode_responses=True)
