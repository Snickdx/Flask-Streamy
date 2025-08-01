import unittest
from flask_streamy.sse import SSE

class TestSSEFeatures(unittest.TestCase):
    def test_multiline_and_retry(self):
        sse = SSE('1', keep_alive_interval=0.1)
        sse.add_message('line1\nline2', event_name='update', event_id=5, retry=5000)
        gen = sse.stream()
        message = next(gen)
        expected = 'id: 5\nevent: update\ndata: line1\ndata: line2\nretry: 5000\n\n'
        self.assertEqual(message, expected)
        sse.end_stream()

    def test_raw_mode(self):
        sse = SSE('raw', keep_alive_interval=0.1)
        raw = 'event: update\ndata: {"val": 5}\nid: 77\nretry: 5000\n\n'
        sse.add_message(raw, raw=True)
        gen = sse.stream()
        message = next(gen)
        self.assertEqual(message, raw)
        sse.end_stream()

if __name__ == '__main__':
    unittest.main()
