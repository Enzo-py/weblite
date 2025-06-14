import json
import warnings

from datetime import datetime

class Message:
    """
        Protocol message class to communicate between the server and the client.
    """

    def __init__(self, content, type="message"):
        self.type = type
        self.content = content

    def __repr__(self):
        content = str(self.content)[:min(50, len(str(self.content)))]
        return f"[Message<{self.type}>]: {content}"
    
    def to_json(self):
          return json.dumps({"type": self.type, "data": {"content": self.content}})
    
    @staticmethod
    def from_json(json_str):
        """
            Dynamically create a message from a json string.
            Can return a different protocole type, but always a protocol class.
        """

        data = json.loads(json_str)

        if "type" not in data or "data" not in data:
            # warning in yellow
            warnings.warn(f"\033[93mInvalid message: {data}\033[0m", stacklevel=3)
            return Error("Invalid message: A message should be compose of a <type> and <data>")

        if data["type"] not in TYPES_MAP or TYPES_MAP[data["type"]] == Message:
            return Message(content=data["data"], type=data["type"])
        
        return TYPES_MAP[data["type"]].from_json(data)
    
class ChunkedMessage:
    ...

class PartialChunkedMessage(Message):
    
    def __init__(self, type, data):
        super().__init__(content=f'PartialChunkedMessage<{type}>', type=type)

        if self.type == 'start_chunked_upload':
            self.start_dt = datetime.now()
            self.upload_id = data['upload_id']
            self.filename = data['filename']
            self.total_chunks = data['total_chunks']
            self.asked_folder = data['folder']

        elif self.type == "chunk":
            self.upload_id = data['upload_id']
            self.chunk_index = data['chunk_index']
            self.bin64 = data['bin64']

    @staticmethod
    def from_json(data):
        return PartialChunkedMessage(data["type"], data['data'])
    
class PopUp(Message):
    def __init__(self, content, callback=None):
        super().__init__(content, type="pop-up")
        self.callback = callback

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "content": self.content,
                "callback": self.callback
            }
        })

    @staticmethod
    def from_json(data):
        pop_up = PopUp(data["data"]["content"], is_open=data["data"]["is_open"])
        pop_up.action = data["data"]["action"]

class Toast(Message):
    def __init__(self, content, toaster_type="success", duration=5000):
        super().__init__(content, type="toast")
        self.duration = duration
        self.toaster_type = toaster_type  # Default type, can be "success", "error", "info", etc.

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "content": self.content,
                "duration": self.duration,
                "type": self.toaster_type,
            }
        })

    @staticmethod
    def from_json(data):
        toast = Toast(data["data"]["content"])
        toast.duration = data["data"]["duration"]
        toast.toaster_type = data["data"]["type"]
        return toast
    
class Notification(Message):
    def __init__(self, content):
        super().__init__(content, type="notification")

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "content": self.content,
            }
        })

    @staticmethod
    def from_json(data):
        notification = Notification(data["data"]["content"])
        return notification
    
class Error(Message):
    def __init__(self, content):
        super().__init__(content, type="error")

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "data": {
                "content": self.content
            }
        })

    @staticmethod
    def from_json(data):
        return Error(data["data"]["content"])

         
TYPES_MAP = {
    # Fondamental types
    "error": Error,
    "message": Message,
    "start_chunked_upload": PartialChunkedMessage,
    "chunk": PartialChunkedMessage,

    # Basic types
    "pop-up": PopUp,
    "toast": Toast,
    "notification": Notification,
}
