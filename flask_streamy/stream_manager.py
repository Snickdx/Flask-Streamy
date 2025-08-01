from flask import Response
from .sse import SSE
import logging

class StreamManager:
    def __init__(self):
        self.streams = {}
        logging.basicConfig(level=logging.INFO)

    def send_event(self, stream_id, data, event_name=None, event_id=None, retry=None, raw=False):
        """Send an event to a given stream.

        Parameters mirror :meth:`SSE.add_message` for convenience."""

        if stream_id in self.streams:
            try:
                self.streams[stream_id].add_message(data, event_name, event_id, retry, raw)
            except Exception as e:
                logging.error(f"Failed to send event to stream {stream_id}: {e}")
        else:
            logging.error(f"Stream {stream_id} does not exist.")
            raise ValueError(f"Stream {stream_id} does not exist.")

    def get_stream(self, stream_id, event_name="message", headers=None, keep_alive_interval=30, start_id=0):
        if stream_id not in self.streams:
            self.streams[stream_id] = SSE(stream_id, event_name, keep_alive_interval, start_id=start_id)
            logging.info(f"Created new stream with ID {stream_id}.")
        sse_instance = self.streams[stream_id]
        response = Response(sse_instance.stream(), content_type='text/event-stream')
        
        # Add default keep-alive header
        response.headers["Connection"] = "keep-alive"
        
        # Add custom headers
        if headers:
            for key, value in headers.items():
                response.headers[key] = value
                
        return response

    def end_stream(self, stream_id):
        if stream_id in self.streams:
            self.streams[stream_id].end_stream()
            del self.streams[stream_id]
        else:
            logging.error(f"Stream {stream_id} does not exist.")
