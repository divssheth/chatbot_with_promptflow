# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum

class ConversationInput:
    def __init__(self, question: str, categories: str, organization_urls: list[str], organization: str):
        self.question = question
        self.categories = categories
        self.organization_urls = organization_urls
        self.organization = organization

class ConversationOutputs:
    """
    Class for storing conversation data.
    """

    def __init__(self, answer: str=None):
        self.answer = answer

class ConversationMessage:
    """
    Class for storing a message in a conversation.
    """

    def __init__(self, inputs: ConversationInput = None, outputs: ConversationOutputs = None):
        self.inputs = inputs
        self.outputs = outputs

class ConversationData:
    """
    Class for storing a log of utterances (text of messages) as a list.
    """

    def __init__(
        self,
        user_id: str = None,
        session_id: str = None,
        messages: list = None,
        timestamp: str = None
    ):
        self.user_id = user_id
        self.session_id = session_id
        self.messages = messages
        self.timestamp = timestamp
