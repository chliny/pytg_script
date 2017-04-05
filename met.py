#!/usr/bin/python
#-*- coding=utf-8 -*-

import logging
import time
import sys

from telegram_python import PyTelegram

class AutoMet(PyTelegram):
    def __init__(self):
        super(AutoMet, self).__init__()
        self.create_test_group()

    def create_test_group(self):
        try:
            self.test_group = "mettest"
            test_groupinfo = self.get_printinfo(self.test_group)
            if not test_groupinfo:
                self_info = self.sender.get_self()
                logging.debug(self_info)
                self_username = self_info["username"]
                self.create_group(self.test_group, [self_username, "enl_jarvis_bot"])
                test_groupinfo = self.get_printinfo(self.test_group)

            self.test_groupid = test_groupinfo["id"]
        except Exception as e :
            logging.error(e)

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

    def met_userlist(self, userlist, group=""):
        if not group:
            group = self.test_group
        for user_dict in userlist:
            try:
                user = user_dict["username"]
                if user in ["chliny", "enl_jarvis_bot"]:
                    continue
                if self.ismeted(user):
                    logging.debug("%s has meted" % user)
                    continue

                logging.debug(user)
                self.met_user(user, group)
            except Exception as e:
                logging.error(e)
        return True

    def ismeted(self, user):
        self.met_user(user, self.test_group)
        history_ret = self.get_history(self.test_groupid, 2)
        metword = "";
        trytimes = 10
        while True and trytimes > 0:
            for chatid, chat_info in history_ret.items():
                try:
                    if chat_info["event"] != "message":
                        continue
                    if "reply_id" not in chat_info:
                        break
                    logging.debug(chat_info)
                    reply_id = chat_info["reply_id"]
                    orig_info = history_ret[reply_id]
                    orig_text = orig_info["text"]
                    if orig_text.find(user) == -1:
                        continue
                    else: 
                        metword = chat_info["text"]
                        break
                except Exception as e:
                    logging.error(e)

            if not metword :
                time.sleep(5)
                history_ret = self.get_history(self.test_groupid, 2)
            else:
                break

            trytimes -= 1

        logging.debug(metword)
        if metword.startswith("您之前已经见过") or metword.startswith("You have already met"):
            return True
        elif metword.startswith("抱歉我并不知道") or metword.startswith("I'm not aware of who"):
            return True
        else:
            logging.debug(metword)
            return False
        return True

    def met_user(self, user, group):
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

