"""Main module for the API app."""

import graphene  # type: ignore

from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor

import schema

app = FastAPI()
app.add_route(
    "/",
    GraphQLApp(
        schema=graphene.Schema(query=schema.Query),
        executor_class=AsyncioExecutor
    )
)
