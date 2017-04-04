#!/usr/bin/python
#-*- coding=utf-8 -*-

import logging
import time
import sys

from telegram_python import PyTelegram

class AutoMet(PyTelegram):
    def __init__(self):
        super(AutoMet, self).__init__()
        self.test_group = "testtgcli"

    def parse_argv(self):
        try:
            target = sys.argv[1]
        except Exception as e:
            logging.error(e)
            return False
        target_info = self.get_printinfo(target)
        if not target_info:
            return False	
        try:
            target_type = target_info["peer_type"]
            printname = target_info["print_name"]
        except Exception as e:
            logging.error(e)

        if target_type == "user":
            return self.met_userlist([target_info])
        else:
            return self.met_group(printname)

    def get_printinfo(self, target):
        dialogs = self.get_dialog_list()
        for dialog_info in dialogs:
            for key in ["title", "username", "print_name"]:
                if key in dialog_info and dialog_info[key] == target:
                    return dialog_info
        return {}

    def met_group(self, group):
        members = self.channel_get_members(group)
        return met_userlist(members,group)

    def met_userlist(self, userlist, group="testtgcli"):
        for user_dict in userlist:
            try:
                user = user_dict["username"]
                if user in ["chliny", "enl_jarvis_bot"]:
                    continue
                logging.debug(user)
                self.met_user(user, group)
            except Exception as e:
                logging.error(e)
        return True

    def met_user(self, group, user):
        try:
            if user.startswith("@"):
                word = "/met %s" % user
            else:
                word = "/met @%s" % user
            self.sender.send_msg(group, word)
        except Exception as e :
            logging.error(e)
            return False
        return True

if __name__ == "__main__":
    automet = AutoMet()
    automet.parse_argv()

