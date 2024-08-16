import pytest
import os
from swarmauri.standard.llms.concrete.MistralModel import MistralModel as LLM
from swarmauri.standard.conversations.concrete.Conversation import Conversation

from swarmauri.standard.messages.concrete.AgentMessage import AgentMessage
from swarmauri.standard.messages.concrete.HumanMessage import HumanMessage
from swarmauri.standard.messages.concrete.SystemMessage import SystemMessage

@pytest.mark.unit
def test_ubc_resource():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    llm = LLM(api_key = API_KEY)
    assert llm.resource == 'LLM'


@pytest.mark.unit
def test_ubc_type():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    llm = LLM(api_key = API_KEY)
    assert llm.type == 'MistralModel'

@pytest.mark.unit
def test_serialization():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    llm = LLM(api_key = API_KEY)
    assert llm.id == LLM.model_validate_json(llm.model_dump_json()).id

@pytest.mark.unit
def test_default_name():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    model = LLM(api_key = API_KEY)
    assert model.name == 'open-mixtral-8x7b'

@pytest.mark.unit
def test_no_system_context():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    model = LLM(api_key = API_KEY)
    conversation = Conversation()

    input_data = "Hello"
    human_message = HumanMessage(content=input_data)
    conversation.add_message(human_message)

    model.predict(conversation=conversation)
    prediction = conversation.get_last().content
    assert type(prediction) == str

@pytest.mark.acceptance
def test_nonpreamble_system_context():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    model = LLM(api_key = API_KEY)
    conversation = Conversation()

    # Say hi
    input_data = "Hi"
    human_message = HumanMessage(content=input_data)
    conversation.add_message(human_message)

    # Get Prediction
    prediction = model.predict(conversation=conversation)

    # Give System Context
    system_context = 'You only respond with the following phrase, "Jeff"'
    human_message = HumanMessage(content=system_context)
    conversation.add_message(human_message)

    # Prompt
    input_data = "Hello Again."
    human_message = HumanMessage(content=input_data)
    conversation.add_message(human_message)


    model.predict(conversation=conversation)
    prediction = conversation.get_last().content
    assert 'Jeff' in prediction


@pytest.mark.unit
def test_preamble_system_context():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    model = LLM(api_key = API_KEY)
    conversation = Conversation()

    system_context = 'You only respond with the following phrase, "Jeff"'
    human_message = HumanMessage(content=system_context)
    conversation.add_message(human_message)

    input_data = "Hi"
    human_message = HumanMessage(content=input_data)
    conversation.add_message(human_message)

    model.predict(conversation=conversation)
    prediction = conversation.get_last().content
    assert type(prediction) == str
    assert 'Jeff' in prediction

@pytest.mark.acceptance
def test_multiple_system_contexts():
    API_KEY = os.getenv('MISTRAL_API_KEY')
    model = LLM(api_key = API_KEY)
    conversation = Conversation()

    system_context = 'You only respond with the following phrase, "Jeff"'
    human_message = HumanMessage(content=system_context)
    conversation.add_message(human_message)

    input_data = "Hi"
    human_message = HumanMessage(content=input_data)
    conversation.add_message(human_message)

    model.predict(conversation=conversation)

    system_context_2 = 'You only respond with the following phrase, "Ben"'
    human_message = HumanMessage(content=system_context_2)
    conversation.add_message(human_message)

    input_data_2 = "Hey"
    human_message = HumanMessage(content=input_data_2)
    conversation.add_message(human_message)

    model.predict(conversation=conversation)
    prediction = conversation.get_last().content
    assert type(prediction) == str
    assert 'Ben' in prediction