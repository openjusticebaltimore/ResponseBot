from unittest.case import TestCase

from responsebot.listeners.tweepy_wrapper_listener import TweepyWrapperListener
from responsebot.models import Event

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


class TweepyWrapperListenerTestCase(TestCase):
    def test_call_generic_listener_on_tweet(self):
        generic_listener = MagicMock(on_tweet=MagicMock())
        status = MagicMock(_json={'some key': 'some value'})

        tweet_obj = 'tweet_obj'
        with patch('responsebot.listeners.tweepy_wrapper_listener.Tweet', return_value=tweet_obj) as mock_tweet_obj:
            TweepyWrapperListener(listener=generic_listener).on_status(status)

            mock_tweet_obj.assert_called_once_with(status._json)
            generic_listener.on_tweet.assert_called_once_with(tweet_obj)

    def test_call_generic_listener_on_event(self):
        generic_listener = MagicMock(on_event=MagicMock())
        event = MagicMock(_json={})
        event_wrapper = Event(event)

        with patch('responsebot.listeners.tweepy_wrapper_listener.Event', return_value=event_wrapper):
            TweepyWrapperListener(listener=generic_listener).on_event(event)

            generic_listener.on_event.assert_called_once_with(event_wrapper)

    def test_call_generic_listener_on_direct_message(self):
        generic_listener = MagicMock(on_direct_message=MagicMock())
        message = MagicMock(_json={'some key': 'some value'})

        message_obj = 'message_obj'
        with patch('responsebot.listeners.tweepy_wrapper_listener.DirectMessage', return_value=message_obj) as mock_message_obj:
            TweepyWrapperListener(listener=generic_listener).on_direct_message(message)

            mock_message_obj.assert_called_once_with(message._json)
            generic_listener.on_direct_message.assert_called_once_with(message_obj)