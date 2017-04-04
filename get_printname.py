#!/usr/bin/python
#-*- coding=utf-8 -*-

import sys
import logging
from telegram_python import PyTelegram

class GetPrintName(PyTelegram):
    def __init__(self):
        super(GetPrintName, self).__init__()

    def parse_dialogs(self, target):
        dialogs = self.get_dialog_list()
        for dialog_info in dialogs:
            for key in ["title", "username"]:
                if key in dialog_info and dialog_info[key] == target:
                    self.print_dict(dialog_info)
                    return True
        return False
    
    def print_dict(self, target_dict):
        for key, value in target_dict.items():
            value = str(value)
            logging.debug("%s:%s" % (key, value))
            print ("%s: %s" % (key, value))

    def parse_channels(self, target):
        channels = self.get_channel_list()
        for channel_info in channels:
            if "title" in channel_info and channel_info["title"] == target:
                self.print_dict(channel_info)
                return True
        return False

    def get_printname(self):
        try:
            target = sys.argv[1]
        except Exception as e:
            logging.error(e)
            return False

        if self.parse_channels(target):
            return True

        if self.parse_dialogs(target):
            return True

        return False

if __name__ == "__main__":
    gpn = GetPrintName()
    gpn.get_printname()

