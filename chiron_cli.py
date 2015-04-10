import readline
import sys

import chiron

class CLIMessage(chiron.Message):
    def __init__(self, body, cls, instance, sender="CLI", recipient=None):
        self._body = body
        self._cls = cls
        self._instance = instance
        self._sender = sender
        self._recipient = recipient
        self._messages = []

    def body(self):
        return self._body

    def cls(self):
        return self._cls

    def instance(self):
        return self._instance

    def sender(self):
        return self._sender

    def recipient(self):
        return self._recipient

    def is_personal(self):
        return bool(self._recipient)

    def send_reply(self, messages):
        self._messages = messages

    @classmethod
    def main(cls, match_engine, options):
        while True:
            try:
                c = raw_input("class: ")
            except (KeyboardInterrupt, EOFError):
                print
                return
            print "Type your message now.  End with control-D or a dot on a line by itself."
            m = ""
            while True:
                try:
                    line = raw_input()
                except KeyboardInterrupt:
                    return
                except EOFError:
                    line = None
                if not line or line.strip() == ".":
                    break
                m += line
            msg = cls(body=m, cls=c, instance="")
            match_engine.process(msg)
            for (response, url) in msg._messages:
                print "URL: {}\nresponse: {}".format(url, response)

def main(match_engine, options):
    CLIMessage.main(match_engine, options)
