"""Shared utilities for MB assignment."""

import motor.motor_asyncio  # type: ignore

HOST = 'localhost'  # normally I'd load this from configuration
PORT = 27017


class MongoCon(object):
    """A singleton Mongo client."""
    __db = None

    @classmethod
    def get_connection(cls, host=HOST, port=PORT):
        if cls.__db is None:
            cls.__db = motor.motor_asyncio.AsyncIOMotorClient(host, port)
        return cls.__db


def get_mongo_client(*args, **kwargs):
    return MongoCon.get_connection(*args, **kwargs)
