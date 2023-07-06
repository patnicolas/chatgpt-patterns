__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from unittest import TestCase
import unittest
from typing import NoReturn, AnyStr
from src.llm.llmconversation import LLMConversation


class TestLLMConversation(TestCase):

    @staticmethod
    def execute_conversation(llm_conversation: LLMConversation, prompt_input: AnyStr) -> NoReturn :
        prompt_input = "What is the color of the moon"
        response = llm_conversation(prompt_input)
        print(f'{prompt_input} => {response}')

    def test_conversation_memory(self):
        llm_conversation = LLMConversation(
            _model="gpt-3.5-turbo-0613",
            memory_buffer_type=LLMConversation.conversation_memory_type,
            argument=4,
            _verbose=True)
        TestLLMConversation.execute_conversation(llm_conversation, "What is the color of the moon")
        TestLLMConversation.execute_conversation(llm_conversation, "How far is the moon from earth")
        TestLLMConversation.execute_conversation(llm_conversation, "How many eclipses of the moon occur every year")

        print(str(llm_conversation.load_memory_variables()))
        llm_conversation.save_context({'color of Neptune': 'blue', 'Moon age': '39123'})
        print(str(llm_conversation.load_memory_variables()))

    @unittest.skip
    def test_token_memory(self):
        llm_conversation = LLMConversation(
            _model="gpt-3.5-turbo-0613",
            memory_buffer_type=LLMConversation.token_memory_type,
            argument=4,
            _verbose=True)
        TestLLMConversation.execute_conversation(llm_conversation, "What is the color of the moon")
        TestLLMConversation.execute_conversation(llm_conversation, "How far is the moon from earth")
        TestLLMConversation.execute_conversation(llm_conversation, "How many eclipses of the moon occur every year")

    @unittest.skip
    def test_entity_memory(self):
        llm_conversation = LLMConversation(
            _model="gpt-3.5-turbo-0613",
            memory_buffer_type=LLMConversation.entity_memory_type,
            argument=4,
            _verbose=True)
        TestLLMConversation.execute_conversation(llm_conversation, "What is the color of the moon")
        TestLLMConversation.execute_conversation(llm_conversation, "How far is the moon from earth")
        TestLLMConversation.execute_conversation(llm_conversation, "How many eclipses of the moon occur every year")
