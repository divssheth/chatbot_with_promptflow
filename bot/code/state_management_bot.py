# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import time
from datetime import datetime

from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.schema import ChannelAccount

from conversation_data import ConversationData, ConversationMessage
from botbuilder.azure import CosmosDbPartitionedStorage, CosmosDbPartitionedConfig
import json
import urllib

class StateManagementBot(ActivityHandler):
    ## Uncomment this for state management
    def __init__(self, conversation_state: ConversationState, llm_endpoint: str, categories: str, organization_urls: list[str], organization: str, llm_api_key: str, welcome_message: str):
        self.llm_endpoint = llm_endpoint
        self.categories = categories
        self.organization_urls = organization_urls
        self.organization = organization
        self.llm_api_key = llm_api_key
        self.welcome_message = welcome_message
        if conversation_state is None:
            raise TypeError(
                "[StateManagementBot]: Missing parameter. conversation_state is required but None was given"
            )
        self.conversation_state = conversation_state
        
        self.conversation_data_accessor = self.conversation_state.create_property("ConversationData")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    self.welcome_message
                )

    async def on_message_activity(self, turn_context: TurnContext):
        # Get the state properties from the turn context.
        # user_profile = await self.user_profile_accessor.get(turn_context, UserProfile)
        conversation_data = await self.conversation_data_accessor.get(
            turn_context, ConversationData
        )

        # Add message details to the conversation data.
        conversation_data.timestamp = self.__datetime_from_utc_to_local(
            turn_context.activity.timestamp
        )
        session_id = turn_context.activity.conversation.id
        user_id = turn_context.activity.from_property.id + "-" + turn_context.activity.channel_id
        conversation_data.session_id = session_id
        conversation_data.user_id = user_id
        if conversation_data.messages is None:
            conversation_data.messages = []
        answer = self.call_llm(turn_context.activity.text, conversation_data.messages)
        # print(answer)
        message = dict()
        # message = ConversationMessage()
        message["inputs"] = {
            "question": turn_context.activity.text,
            "categories": self.categories,
            "organization_urls": self.organization_urls,
            "organization": self.organization,
        }
        message["outputs"] = json.loads(answer)
        conversation_data.messages.append(message)
        await turn_context.send_activity(
            message["outputs"]["answer"]
        )
        
        

    def __datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
            now_timestamp
        )
        result = utc_datetime + offset
        return result.strftime("%I:%M:%S %p, %A, %B %d of %Y")
    
    def call_llm(self, question, chat_history = []):
        data = dict()
        data["question"] = question
        data["chat_history"] = chat_history
        data["categories"] = self.categories
        data["organization_urls"] = self.organization_urls
        data["organization"] = self.organization

        body = str.encode(json.dumps(data))

        # Replace this with the primary/secondary key or AMLToken for the endpoint
        api_key = self.llm_api_key
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        # The azureml-model-deployment header will force the request to go to a specific deployment.
        # Remove this header to have the request observe the endpoint traffic rules
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'chat-with-website-1' }

        req = urllib.request.Request(self.llm_endpoint, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            # print(result)
            return result
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))