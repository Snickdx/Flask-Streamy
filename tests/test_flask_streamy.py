import unittest
from flask_streamy.stream_manager import StreamManager
from flask import Flask, Response

class TestStreamManager(unittest.TestCase):
    def setUp(self):
        self.sse = StreamManager()

    def test_create_and_get_stream(self):
        response = self.sse.get_stream("test")
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/event-stream")
        self.assertEqual(response.headers["Connection"], "keep-alive")

    def test_send_event(self):
        self.sse.get_stream("test")
        self.sse.send_event("test", "Hello, World!", event_name="greeting")
        # Assuming we have a way to consume the event, we'd test the output here

    def test_end_stream(self):
        self.sse.get_stream("test")
        self.sse.end_stream("test")
        with self.assertRaises(ValueError):
            self.sse.send_event("test", "This should fail")

    def test_custom_headers(self):
        headers = {
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache"
        }
        response = self.sse.get_stream("test", headers=headers)
        self.assertEqual(response.headers["X-Accel-Buffering"], "no")
        self.assertEqual(response.headers["Cache-Control"], "no-cache")

    def test_keep_alive_messages(self):
        # Create a stream with a short keep-alive interval for testing
        response = self.sse.get_stream("test", keep_alive_interval=1)
        self.assertIsInstance(response, Response)
        # Simulate consuming the response stream and ensure keep-alive messages are sent

    def test_logging_and_error_handling(self):
        self.sse.get_stream("test")
        # Induce an error by trying to send an event to a non-existent stream
        with self.assertLogs(level='ERROR') as log:
            self.sse.send_event("non_existent_stream", "This should log an error")
        self.assertIn("ERROR:root:Stream non_existent_stream does not exist.", log.output)

    def test_error_retry_logic(self):
        # Assuming there's a method to simulate errors and retries in the SSE class
        self.sse.get_stream("test")
        with self.assertLogs(level='ERROR') as log:
            # Simulate an error to trigger retry logic
            self.sse.send_event("test", "Trigger error", event_name="error_event")
            # Note: this requires mock or a mechanism to simulate the error in SSE
        self.assertIn("ERROR:root:Stream test encountered an error", log.output)
        self.assertIn("INFO:root:Stream test retrying", log.output)

if __name__ == '__main__':
    unittest.main()
