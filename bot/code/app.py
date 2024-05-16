# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
# import os

# current = os.path.dirname(os.path.realpath(__file__))
# # Getting the parent directory name where the current directory is present.
# parent = os.path.dirname(current)
# # adding the parent directory to the sys.path.
# sys.path.append(parent)

import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.azure import CosmosDbPartitionedStorage, CosmosDbPartitionedConfig

from state_management_bot import StateManagementBot
from config import DefaultConfig

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))

# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)

    # Clear out state
    await CONVERSATION_STATE.delete(context)


# Set the error handler on the Adapter.
# In this case, we want an unbound method, so MethodType is not needed.
ADAPTER.on_turn_error = on_error

if CONFIG.ADD_COSMOS_MEMORY.lower() == "true":
    cosmos_config = CosmosDbPartitionedConfig(
                cosmos_db_endpoint=CONFIG.COSMOS_DB_URI,
                auth_key=CONFIG.COSMOS_DB_PRIMARY_KEY,
                database_id=CONFIG.COSMOS_DB_DATABASE_ID,
                container_id=CONFIG.COSMOS_DB_CONTAINER_ID,
                compatibility_mode = False
            )
    # Create CosmosDbPartitionedStorage with CosmosDbPartitionedConfig
    MEMORY = CosmosDbPartitionedStorage(cosmos_config)
else:
    MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)

# Create Bot
BOT = StateManagementBot(CONVERSATION_STATE, llm_endpoint=CONFIG.LLM_APP_ENDPOINT, categories=CONFIG.CATEGORIES, organization_urls=CONFIG.ORGANIZATION_URLS, organization=CONFIG.ORGANIZATION, llm_api_key=CONFIG.LLM_API_KEY, welcome_message=CONFIG.WELCOME_MESSAGE)

# Listen for incoming requests on /api/messages.
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(auth_header, activity, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

def health(request):
    return web.Response(text="healthy")

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)
APP.router.add_get("/api/health", health)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error