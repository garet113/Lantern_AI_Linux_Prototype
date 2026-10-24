import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
spec = importlib.util.spec_from_file_location('chat', Path(__file__).parents[1]/'app/lantern_ai.py')
chat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chat)
class ChatTests(unittest.TestCase):
    def response(self, data):
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value = json.dumps(data).encode()
        return opener

    def test_local_protocol_and_proxy_bypass(self):
        opener = self.response({'message': {'content': 'hello'}})
        with patch.object(chat.urllib.request, 'build_opener', return_value=opener) as factory:
            self.assertEqual(chat.request_reply('test', [{'role':'user','content':'hi'}]), 'hello')
            self.assertEqual(factory.call_args.args[0].proxies, {})
            req=opener.open.call_args.args[0]
            self.assertEqual(req.full_url, 'http://127.0.0.1:11434/api/chat')
            payload=json.loads(req.data)
            self.assertFalse(payload['stream'])
            self.assertEqual(payload['messages'], [{'role':'user','content':'hi'}])
            self.assertEqual(payload['model'], 'test')

    def test_failure_propagates(self):
        opener = MagicMock()
        opener.open.side_effect = OSError('offline')
        with patch.object(chat.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaises(OSError): chat.request_reply('test', [])

    def test_rejects_non_text_response(self):
        with patch.object(chat.urllib.request, 'build_opener', return_value=self.response({'message': {'content': None}})):
            with self.assertRaises(ValueError): chat.request_reply('test', [])

    def test_invalid_json(self):
        opener = self.response({})
        opener.open.return_value.__enter__.return_value.read.return_value = b'not json'
        with patch.object(chat.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaises(json.JSONDecodeError): chat.request_reply('test', [])

if __name__ == '__main__': unittest.main()
