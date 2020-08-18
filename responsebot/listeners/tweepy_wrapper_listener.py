from tweepy.streaming import StreamListener

from responsebot.models import Tweet, Event, DirectMessage


class TweepyWrapperListener(StreamListener):
    def __init__(self, listener, *args, **kwargs):
        super(TweepyWrapperListener, self).__init__(*args, **kwargs)

        self.listener = listener

    def on_status(self, status):
        self.listener.on_tweet(Tweet(status._json))

    def on_event(self, event):
        self.listener.on_event(Event(event._json))

    def on_direct_message(self, message):
        self.listener.on_direct_message(DirectMessage(message._json))