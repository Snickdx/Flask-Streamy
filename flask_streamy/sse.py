import time
import logging
from queue import Queue, Empty

class SSE:
    def __init__(self, stream_id, event_name="message", keep_alive_interval=30, max_retries=3):
        self.stream_id = stream_id
        self.event_name = event_name
        self.queue = Queue()
        self.active = True
        self.keep_alive_interval = keep_alive_interval  # Interval for keep-alive messages
        self.max_retries = max_retries  # Max retries on error
        self.retry_count = 0  # Track retries
        logging.basicConfig(level=logging.INFO)

    def add_message(self, data, event_name=None):
        if event_name is None:
            event_name = self.event_name
        if self.active:
            self.queue.put((event_name, data))
            self.retry_count = 0  # Reset retries on successful message addition
            logging.info(f"Stream {self.stream_id} - Event {event_name}: {data}")

    def end_stream(self):
        self.active = False
        self.queue.put((None, None))  # Sentinel to end the stream
        logging.info(f"Stream {self.stream_id} ended.")

    def handle_error(self, error):
        logging.error(f"Stream {self.stream_id} encountered an error: {error}")
        self.retry_count += 1
        if self.retry_count > self.max_retries:
            logging.error(f"Stream {self.stream_id} exceeded max retries. Ending stream.")
            self.end_stream()
        else:
            logging.info(f"Stream {self.stream_id} retrying ({self.retry_count}/{self.max_retries})...")

    def stream(self):
        last_event_time = time.time()
        while self.active:
            try:
                event_name, data = self.queue.get(timeout=self.keep_alive_interval)
                if event_name is None:
                    break  # Exit loop if stream is ended
                yield f"id: {self.stream_id}\nevent: {event_name}\ndata: {data}\n\n"
                last_event_time = time.time()
            except Empty:
                # Send a comment line as a keep-alive message
                yield f": keep-alive\n\n"
                last_event_time = time.time()
            except Exception as e:
                self.handle_error(e)
