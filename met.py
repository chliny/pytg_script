#!/usr/bin/python
#-*- coding=utf-8 -*-

import logging

from telegram_python import PyTelegram
from get_printname import GetPrintName

class AutoMet(PyTelegram):
    def __init__(self):
        super(AutoMet, self).__init__()
        self.gp = GetPrintName()
        

    def parse_argv(self):
        try:
            target = sys.argv[1]
        except Exception as e:
            logging.error(e)
            return False
        group_printname = self.gp.get_printname(target)
        if not group_printname:
            return False	
        return self.met_group(group_printname)


    def met_group(self, group):
        members = self.channel_get_members(group)
        for user_dict in members:
            try:
                user = user_dict["username"]
                if user in ["chliny", "enl_jarvis_bot"]:
                    continue
                logging.debug(user)
                self.met_user(group, user)
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

