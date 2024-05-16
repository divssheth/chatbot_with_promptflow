#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    COSMOS_DB_URI = os.environ.get("COSMOS_DB_URI", "")
    COSMOS_DB_PRIMARY_KEY = os.environ.get("COSMOS_DB_PRIMARY_KEY", "")
    COSMOS_DB_DATABASE_ID = os.environ.get("COSMOS_DB_DATABASE_ID", "")
    COSMOS_DB_CONTAINER_ID = os.environ.get("COSMOS_DB_CONTAINER_ID", "")
    LLM_APP_ENDPOINT = os.environ.get("LLM_APP_ENDPOINT", "")
    LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
    CATEGORIES = os.environ.get("CATEGORIES", "")
    ORGANIZATION_URLS = os.environ.get("ORGANIZATION_URLS", "").split(",")
    ORGANIZATION = os.environ.get("ORGANIZATION", "")
    ADD_COSMOS_MEMORY = os.environ.get("ADD_COSMOS_MEMORY", "")
    WELCOME_MESSAGE = os.environ.get("WELCOME_MESSAGE", "Welcome to Chatty")