# Flask Streamy

`flask-streamy` is a lightweight Flask package that provides an abstraction for managing Server-Sent Events (SSE) streams. It allows you to easily create, manage, and terminate event streams in your Flask applications.

## Installation

```bash
pip install flask-streamy
```

## Basic Usage
```python
from flask import Flask
from flask_streamy import StreamManager

app = Flask(__name__)
sse = StreamManager()

@app.route('/send_event')
def send_event():
    sse.send_event("stream1", data="Hello, World!", event_name="greeting")
    return "Event sent"

@app.route('/stream')
def events():
    headers = {
        "X-Accel-Buffering": "no",  # Disable response buffering
        "Cache-Control": "no-cache"
    }
    return sse.get_stream("stream1", headers=headers)

@app.route('/end_stream')
def end_stream():
    sse.end_stream("stream1")
    return "Stream ended"

if __name__ == "__main__":
    app.run(debug=True)
```

### Advanced Usage

You can control event IDs, retry delays, multi-line payloads, or even supply
fully formatted SSE messages yourself:

```python
@app.route('/advanced')
def advanced_send():
    # Multi-line data and custom retry delay
    sse.send_event(
        "stream1",
        data="line1\nline2",
        event_name="update",
        event_id=10,
        retry=5000,
    )

    # Raw mode bypasses formatting completely
    raw = "event: update\ndata: {\"val\": 5}\nid: 77\nretry: 5000\n\n"
    sse.send_event("stream1", raw, raw=True)
    return "Sent advanced events"
```

## API

**StreamManager**

*   get_stream(stream_id, event_name="message", headers=None, keep_alive_interval=30, start_id=0):
    *   Retrieves or creates a stream for the given ID.
    *   Allows setting custom headers and a keep-alive interval to maintain the connection.
    *   Supports resuming with a custom starting event ID.
    *   Automatically sends a Connection: keep-alive header and periodic keep-alive messages.
*   send_event(stream_id, data, event_name=None, event_id=None, retry=None, raw=False):
    *   Sends an event to the specified stream with options for custom IDs,
        reconnect delays, and raw message delivery.
    *   Automatically handles errors with logging and retry logic.
*   end_stream(stream_id):
    *   Ends the stream for the given ID.
    *   Logs the termination of the stream.

**SSE**
*   Logging:
    *   Logs key events like stream creation, message addition, and stream termination.
*   Error Handling with Retries:
    *   Automatically retries sending events up to a configurable number of times before ending the stream.
*   Keep-Alive Messages:
    *   Periodic keep-alive messages are sent to prevent connection timeouts during idle periods.
*   Custom Event IDs:
    *   Set starting IDs and resume from custom IDs.
*   Manual Retry Delays:
    *   Control the `retry` field sent to clients when reconnecting.
*   Multiline Data:
    *   Payloads can contain line breaks and are formatted correctly for SSE.
*   Raw Mode:
    *   Optionally queue pre-formatted SSE strings for full control.

## Testing

Here's an updated section for the `README.md` to include instructions on how to test the `flask-streamy` package:


### Running Tests

Tests for `flask-streamy` are located in the `tests` directory. To run the tests, you'll need to have `unittest` available, which is included in the Python standard library.

You can run the tests by executing the following command in the root of the package:

```bash
python -m unittest discover tests
```

### Writing Tests

The `tests/test_flask_streamy.py` file contains example unit tests that check the core functionality of `flask-streamy`. Here’s a brief overview of what the tests cover:

- **Stream Creation and Retrieval**: Ensures that streams are correctly created and retrieved by `get_stream`.
- **Sending Events**: Validates that events are correctly added to the stream's message queue.
- **Ending Streams**: Confirms that streams can be properly terminated and are no longer accessible after being ended.

You can add your own tests to the `tests` directory to cover additional use cases or to test custom functionality you may add to the package.
