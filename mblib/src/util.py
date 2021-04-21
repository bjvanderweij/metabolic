"""Shared utilities for MB assignment."""

import motor.motor_asyncio  # type: ignore
import settings

class MongoCon(object):
    """A singleton Mongo client."""
    __db = None

    @classmethod
    def get_connection(
            cls,
            host=settings.MONGODB_HOST,
            port=settings.MONGODB_PORT
            ):
        if cls.__db is None:
            cls.__db = motor.motor_asyncio.AsyncIOMotorClient(host, port)
        return cls.__db


def get_mongo_client(*args, **kwargs):
    return MongoCon.get_connection(*args, **kwargs)
