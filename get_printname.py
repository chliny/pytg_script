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
                    return dialog_info["print_name"]
        return ""
    
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
                return channel_info["print_name"]
        return False

    def parse_argv(self):
        try:
            target = sys.argv[1]
        except Exception as e:
            logging.error(e)
            return False
        return self.get_printname(target)

    def get_printname(self, target):
        print_name = self.parse_channels(target)
        if print_name:
            return print_name

        print_name = self.parse_dialogs(target)
        if print_name:
            return print_name

        return ""

if __name__ == "__main__":
    gpn = GetPrintName()
    gpn.parse_argv()

