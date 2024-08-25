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

@app.route('/send_event/<stream_id>')
def send_event(stream_id):
    sse.send_event(stream_id, data="Hello, World!", event_name="greeting")
    return f"Event sent to stream {stream_id}"

@app.route('/events/<stream_id>')
def events(stream_id):
    return sse.get_stream(stream_id)

@app.route('/end_stream/<stream_id>')
def end_stream(stream_id):
    sse.end_stream(stream_id)
    return f"Stream {stream_id} ended"

if __name__ == "__main__":
    app.run(debug=True)
```

## API

**StreamManager**

* get_stream(stream_id, event_name="message"): Retrieves or creates a stream for the given ID.

* send_event(stream_id, data, event_name=None): Sends an event to the 
specified stream.
* end_stream(stream_id): Ends the stream for the given ID.

**SSE**
* add_message(data, event_name=None): Adds a message to the stream.
* end_stream(): Ends the stream.

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
