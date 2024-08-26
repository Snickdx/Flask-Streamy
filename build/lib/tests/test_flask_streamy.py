import unittest
from flask_streamy.stream_manager import StreamManager

class TestStreamManager(unittest.TestCase):
    def setUp(self):
        self.sse = StreamManager()

    def test_create_and_get_stream(self):
        stream = self.sse.get_stream("test")
        self.assertIsNotNone(stream)

    def test_send_event(self):
        self.sse.get_stream("test")
        self.sse.send_event("test", "Hello, World!")
        # Further testing could be done by consuming the stream

    def test_end_stream(self):
        self.sse.get_stream("test")
        self.sse.end_stream("test")
        with self.assertRaises(ValueError):
            self.sse.send_event("test", "This should fail")

if __name__ == '__main__':
    unittest.main()
