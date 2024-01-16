import redis
from environs import Env

env = Env()
env.read_env()

questions_redis = redis.Redis(
    host=env.str("HOST"),
    port=env.int("PORT", 6379),
    db=env.int("QUESTIONS_DB", 0),
    password=env.int("QUESTIONS_DB_PASSWORD", None),
    decode_responses=True,
)

users_redis = redis.Redis(
    host=env.str("HOST"),
    port=env.int("PORT", 6379),
    db=env.int("QUESTIONS_DB", 1),
    password=env.int("USERS_DB_PASSWORD", None),
    decode_responses=True,
)

points_redis = redis.Redis(
    host=env.str("HOST"),
    port=env.int("PORT", 6379),
    db=env.int("QUESTIONS_DB", 2),
    password=env.int("POINTS_DB_PASSWORD", None),
    decode_responses=True,
)
