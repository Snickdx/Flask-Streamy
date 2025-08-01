import time
import logging
from queue import Queue, Empty

class SSE:
    def __init__(self, stream_id, event_name="message", keep_alive_interval=30,
                 max_retries=3, start_id=0):
        """Create a new :class:`SSE` stream.

        Parameters
        ----------
        stream_id: str
            Identifier for the stream.
        event_name: str, optional
            Default event name used if none is supplied when ``add_message`` is
            called.
        keep_alive_interval: int, optional
            Interval in seconds for sending keep alive comments.
        max_retries: int, optional
            Maximum number of times to retry sending before the stream is
            closed if errors occur.
        start_id: int, optional
            Starting event id for the stream. This allows clients to resume from
            a specific id.
        """

        self.stream_id = stream_id
        self.event_name = event_name
        self.queue = Queue()
        self.active = True
        self.keep_alive_interval = keep_alive_interval  # Interval for keep-alive messages
        self.max_retries = max_retries  # Max retries on error
        self.retry_count = 0  # Track retries
        self.last_id = start_id
        logging.basicConfig(level=logging.INFO)

    def add_message(self, data, event_name=None, event_id=None, retry=None, raw=False):
        """Queue a message for the stream.

        Parameters
        ----------
        data: str
            The payload for the ``data`` field or the full raw message when
            ``raw`` is ``True``.
        event_name: str, optional
            Name of the event. If omitted the default event name for the stream
            is used.
        event_id: int or str, optional
            Custom id to send with the event. When ``None`` an incrementing id is
            used.
        retry: int, optional
            Custom reconnect delay in milliseconds to send with the ``retry``
            field.
        raw: bool, optional
            When ``True`` ``data`` is expected to contain a fully formatted SSE
            string and will be queued without any processing.
        """

        if event_name is None:
            event_name = self.event_name
        if self.active:
            self.queue.put({
                "event": event_name,
                "data": data,
                "id": event_id,
                "retry": retry,
                "raw": raw,
            })
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
        """Generator yielding formatted SSE messages."""
        last_event_time = time.time()
        while self.active:
            try:
                msg = self.queue.get(timeout=self.keep_alive_interval)
                if not isinstance(msg, dict):
                    break  # Sentinel or old style data
                if msg.get("raw"):
                    data = msg["data"]
                    if not data.endswith("\n\n"):
                        data += "\n\n"
                    yield data
                    last_event_time = time.time()
                    continue

                event_name = msg.get("event", self.event_name)
                data = msg.get("data", "")

                event_id = msg.get("id")
                if event_id is None:
                    self.last_id += 1
                    event_id = self.last_id
                else:
                    self.last_id = event_id

                retry = msg.get("retry")

                lines = [f"id: {event_id}", f"event: {event_name}"]
                for line in str(data).splitlines() or [""]:
                    lines.append(f"data: {line}")
                if retry is not None:
                    lines.append(f"retry: {retry}")
                lines.append("")
                yield "\n".join(lines) + "\n"
                last_event_time = time.time()
            except Empty:
                # Send a comment line as a keep-alive message
                yield ": keep-alive\n\n"
                last_event_time = time.time()
            except Exception as e:
                self.handle_error(e)
