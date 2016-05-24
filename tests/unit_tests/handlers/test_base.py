from unittest.case import TestCase

from responsebot.common.exceptions import UserHandlerError
from responsebot.handlers.base import BaseTweetHandler
from responsebot.handlers.event import BaseEventHandler

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


class Handler(BaseTweetHandler):
    class ValidEventHandler(BaseEventHandler):
        pass

    def __init__(self, *args, **kwargs):
        self.event_handler_class = self.ValidEventHandler
        super(Handler, self).__init__(*args, **kwargs)


class HandlerWithInvalidEventHandler(BaseTweetHandler):
    class InvalidEventHandler(object):
        pass

    def __init__(self, *args, **kwargs):
        self.event_handler_class = self.InvalidEventHandler
        super(HandlerWithInvalidEventHandler, self).__init__(*args, **kwargs)


class HandlerWithErrorneousEventHandler(BaseTweetHandler):
    class ErrorneousEventHandler(BaseEventHandler):
        def __init__(self, client):
            raise Exception

    def  __init__(self, *args, **kwargs):
        self.event_handler_class = self.ErrorneousEventHandler
        super(HandlerWithErrorneousEventHandler, self).__init__(*args, **kwargs)


class BaseTweetHandlerTestCase(TestCase):
    def test_register_event_handler_on_user_stream(self):
        client = MagicMock(config={'user_stream': True})

        handler = Handler(client)

        self.assertTrue(isinstance(handler.event_handler, Handler.ValidEventHandler))

    def test_not_register_event_handler_on_public_stream(self):
        client = MagicMock(config={'user_stream': False})

        handler = Handler(client)

        self.assertIsNone(handler.event_handler)

    def test_only_register_valid_event_handler(self):
        client = MagicMock(config={'user_stream': True})

        handler = HandlerWithInvalidEventHandler(client)

        self.assertIsNone(handler.event_handler)

    def test_raise_user_handler_error_on_event_handler_init_error(self):
        client = MagicMock(config={'user_stream': True})

        self.assertRaises(UserHandlerError, HandlerWithErrorneousEventHandler, client=client)
