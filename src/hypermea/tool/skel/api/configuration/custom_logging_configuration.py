"""
Customize the additional_log_configuration() function however you like.
The log setup will call that function as part of its initialization.

Learn more about the python logger here:
https://docs.python.org/3/howto/logging.html
"""
import logging
from hypermea.core.utils import get_logging_handler_by_name, EmojiFormatter


def additional_log_configuration():
    pass

    # add any additional configuration to logging here
    # e.g., to add emojis to the console log uncomment the following:

    # console_handler = get_logging_handler_by_name('console')
    # console_handler.setFormatter(EmojiFormatter('%(asctime)s - %(name)s - %(levelname)s %(message)s'))
