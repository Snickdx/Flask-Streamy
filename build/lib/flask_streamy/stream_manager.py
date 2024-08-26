from flask import Response
from .sse import SSE

class StreamManager:
    def __init__(self):
        self.streams = {}

    def send_event(self, stream_id, data, event_name=None):
        if stream_id in self.streams:
            self.streams[stream_id].add_message(data, event_name)
        else:
            raise ValueError(f"Stream {stream_id} does not exist.")

    def get_stream(self, stream_id, event_name="message"):
        if stream_id not in self.streams:
            self.streams[stream_id] = SSE(stream_id, event_name)
        sse_instance = self.streams[stream_id]
        return Response(sse_instance.stream(), content_type='text/event-stream')

    def end_stream(self, stream_id):
        if stream_id in self.streams:
            self.streams[stream_id].end_stream()
            del self.streams[stream_id]
        else:
            raise ValueError(f"Stream {stream_id} does not exist.")
