#!/usr/bin/python
#-*- coding=utf-8 -*-

import logging
import sys
import time
from telegram_python import PyTelegram
global metlist
metlist=[]
class ReplyMet(PyTelegram):
    def __init__(self):
        super(ReplyMet, self).__init__()
        self.listened_list = []
        self.dialogs = self.get_dialog_list()

    def print_help(self):
        print("python3 %s [ingress_id] [groupname1] [groupname2] ..." \
                % __file__)

    def get_dialoginfo(self, target):
        for dialog_info in self.dialogs:
            for key in ["title", "username", "print_name"]:
                if key in dialog_info and dialog_info[key] == target:
                    return dialog_info
        return {}

    def parse_argv(self):
        if len(sys.argv) < 2:
            return self.print_help()

        try:
            ingress_id = sys.argv[1].lower()
            self.selfname = [ingress_id]
            self_info = self.sender.get_self()
            self_username = self_info["username"].lower()
            self.selfname.append("@"+self_username)
            logging.debug(self.selfname)
        except Exception as e :
            logging.error(e)
            return False

        if len(sys.argv) > 2:
            for group in sys.argv[2:]:
                try:
                    group_info = self.get_dialoginfo(group)
                    self.listened_list.append(group_info["id"])
                except Exception as e:
                    logging.error(e)
        self.receive_loop()
        return True

    def met(self, username, group,mettype):
        try:
            word = "/met @%s" % username
            if mettype==0 :
                word= u"@%s Please only met me once!" % username
            self.sender.send_msg(group, word)
        except Exception as e:
            logging.error(e)
            return False
        return True

    def parse_recive(self, msg_dict):
        try:
            if msg_dict["event"] != "message":
                return False
        except Exception as e:
            logging.error(e)
            logging.debug(msg_dict)
            return False

        try:
            receive_info = msg_dict["receiver"]
            receive_type = receive_info["type"]
            if receive_type not in ["channel", "chat"] \
                    or (receive_type == "chat" and  receive_info["members_num"] <= 2):
                return False
        except Exception as e:
            logging.error(e)
            logging.debug(msg_dict)
            return False

        try:
            if "own" in msg_dict and msg_dict["own"]:
                return False
            if "mention" in msg_dict and not msg_dict["mention"]:
                return False
        except Exception as e:
            logging.error(e)
            logging.debug(msg_dict)
            return False

        try:
            logging.debug(msg_dict)
            sender_info = msg_dict["sender"]
            receiver_id = msg_dict["receiver"]["id"]
        except Exception as e:
            logging.error(e)
            logging.debug(msg_dict)
            return False

        if self.listened_list and receiver_id not in self.listened_list:
            return False

        try:
            msg_text = msg_dict["text"]
            msg_split = msg_text.strip().split()
            if len(msg_split)>=2 and msg_split[0].lower() == "/met" and msg_split[1].lower() in self.selfname:
				if sender_info["username"] in metlist:
					self.met(sender_info["username"], receiver_id,0)
					logging.debug('\n')
					logging.debug('\n')
					logging.debug('\n')
				else:
					self.met(sender_info["username"], receiver_id,1)
					f=open("metlist.txt","a")
					f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
					f.write('\t')
					f.write(sender_info["username"])
					f.write('\n')
					if len(metlist)>=100 :
						del metlist[0]
						metlist.append(sender_info["username"])
					else :
						metlist.append(sender_info["username"])
        except Exception as e :
            logging.error(e)
            return False
        return True

if __name__ == "__main__":
    rm = ReplyMet()
    rm.parse_argv()
