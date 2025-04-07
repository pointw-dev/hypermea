"""
Customize the additional_log_configuration() function however you like.
The log setup will call that function as part of its initialization.

Learn more about the python logger here:
https://docs.python.org/3/howto/logging.html
"""
import logging


LEVEL_EMOJIS = {
    'TRACE': '🐾',
    'DEBUG': '🔍',
    'INFO': 'ℹ️',
    'WARNING': '⚠️',
    'ERROR': '❌',
    'CRITICAL': '🚨'
}


class EmojiFormatter(logging.Formatter):
    def format(self, record):
        emoji = LEVEL_EMOJIS.get(record.levelname, '')
        record.msg = f' {emoji}  {record.msg}'
        return super().format(record)


def additional_log_configuration():
    logger = logging.getLogger()
    handler = [x for x in logger.handlers if x.name == 'console'][0]

    # e.g. uncomment out the next line to add emojis to your console log
    # handler.setFormatter(EmojiFormatter('%(asctime)s - %(name)s - %(levelname)s %(message)s'))
