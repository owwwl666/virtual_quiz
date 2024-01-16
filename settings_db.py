import redis
from environs import Env

env = Env()
env.read_env()

questions_redis = redis.Redis(
    host=env.str("HOST"),
    port=env.int("PORT"),
    db=env.int("QUESTIONS_DB"),
    decode_responses=True,
)

users_redis = redis.Redis(
    host=env.str("HOST"),
    port=env.int("PORT"),
    db=env.int("USERS_DB"),
    decode_responses=True,
)

points_redis = redis.Redis(
    host=env.str("HOST"),
    port=env.int("PORT"),
    db=env.int("POINTS_DB"),
    decode_responses=True,
)
