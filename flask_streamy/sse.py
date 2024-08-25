import time
from queue import Queue

class SSE:
    def __init__(self, stream_id, event_name="message"):
        self.stream_id = stream_id
        self.event_name = event_name
        self.queue = Queue()
        self.active = True

    def add_message(self, data, event_name=None):
        if event_name is None:
            event_name = self.event_name
        if self.active:
            self.queue.put((event_name, data))

    def end_stream(self):
        self.active = False
        self.queue.put((None, None))  # Sentinel to end the stream

    def stream(self):
        while self.active:
            event_name, data = self.queue.get()
            if event_name is None:
                break  # Exit loop if stream is ended
            yield f"id: {self.stream_id}\nevent: {event_name}\ndata: {data}\n\n"
            time.sleep(1)
