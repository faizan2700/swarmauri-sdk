import json
from typing import List, Literal, Dict
from mistralai.client import MistralClient
from swarmauri.core.typing import SubclassUnion

from swarmauri.standard.messages.base.MessageBase import MessageBase
from swarmauri.standard.messages.concrete.AgentMessage import AgentMessage
from swarmauri.standard.llms.base.LLMBase import LLMBase

class MistralModel(LLMBase):
    api_key: str
    allowed_models: List[str] = ['open-mistral-7b', 
    'open-mixtral-8x7b', 
    'open-mixtral-8x22b', 
    'mistral-small-latest',
    'mistral-medium-latest',
    'mistral-large-latest',
    'codestral'
    ]
    name: str = "open-mixtral-8x7b"
    type: Literal['MistralModel'] = 'MistralModel'

    def _format_messages(self, messages: List[SubclassUnion[MessageBase]]) -> List[Dict[str, str]]:
        message_properties = ['content', 'role']
        formatted_messages = [message.model_dump(include=message_properties, exclude_none=True) for message in messages]
        return formatted_messages

    def predict(self, 
        conversation, 
        temperature: int = 0.7, 
        max_tokens: int = 256, 
        top_p: int = 1,
        enable_json: bool=False, 
        safe_prompt: bool=False):
        
        formatted_messages = self._format_messages(conversation.history)

        client =  MistralClient(api_key=self.api_key)        
        if enable_json:
            response = client.chat(
                model=self.name,
                messages=formatted_messages,
                temperature=temperature,
                response_format={ "type": "json_object" },
                max_tokens=max_tokens,
                top_p=top_p,
                safe_prompt=safe_prompt
            )
        else:
            response = client.chat(
                model=self.name,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,                
                safe_prompt=safe_prompt
            )
        
        result = json.loads(response.json())
        message_content = result['choices'][0]['message']['content']
        conversation.add_message(AgentMessage(content=message_content))

        return conversation