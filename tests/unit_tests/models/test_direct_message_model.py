from unittest.case import TestCase

from dateutil.parser import parse

from responsebot.models import DirectMessage


class DirectMessageModelTestCase(TestCase):
    def test_create_from_raw_data(self):
        raw = {
            'some_key': 'some value',
            'type': 'message_create',
            'id': '1295751832384483332',
            'created_timestamp': '1597766285402',
            'message_create': {
                'target': {
                    'recipient_id': '123456789'
                },
                'sender_id': '987654321',
                'message_data': {
                    'text': 'some text',
                    'entities': {
                        'hashtags': [],
                        'symbols': [],
                        'user_mentions': [],
                        'urls': []
                    }
                }
            }
        }

        message = DirectMessage(raw)

        self.assertEqual(message.some_key, 'some value')
        self.assertEqual(message.message_create['message_data']['text'], 'some text')
