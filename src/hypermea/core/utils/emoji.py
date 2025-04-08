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
