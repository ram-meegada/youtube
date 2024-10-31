from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.exceptions import StopConsumer
from channels.consumer import SyncConsumer

class ProgressUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.uuid = self.scope['url_route']['kwargs']["uuid"]
        await self.channel_layer.group_add(self.uuid, self.channel_name)
        await self.accept()

    async def update_type(self, event):
        await self.send(text_data = event["msg"])


class MySyncChatBot(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
    def websocket_receive(self, event):
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        from abstractbaseuser_project import settings
        from io import BytesIO
        from PyPDF2 import PdfReader

        google_api_key = settings.GOOGLE_API_KEY
        # text_data = json.loads(text_data)
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        with open("Nature.pdf" , "rb") as file:
            pdf_text = ""
            pdf_stream = BytesIO(file.read())
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text().strip() + " "
        message = HumanMessage(
            content=[
                {"type": "text",
                    "text": f"generate a summary of the input I provide you and the length of the summary should be strictly atleast 2000 words and give me only text no * and extra symbols"},
                {"type": "text", "text": pdf_text}
            ]
        )
        full_response = ""
        for chunk in llm.stream([message]):
            stream_chunk = chunk.content
            self.send({
            'type': 'websocket.send',
            'text': json.dumps({"data": stream_chunk, "signal": 1})
        })
            full_response += stream_chunk

    def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()