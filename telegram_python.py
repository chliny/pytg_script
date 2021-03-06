#!/usr/bin/python
#-*- coding=utf-8 -*-

import logging
import os
import sys
import socket
import collections
import time
import subprocess

from pytg import Telegram
from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine


class PyTelegram(object):
    def __init__(self):
        tgcli_port = 4458
        self.setlog()
        if not self.start(tgcli_port):
            sys.exit(1)

        self.receiver = Receiver(host="localhost", port=tgcli_port)
        self.sender = Sender(host="localhost", port=tgcli_port)

    def setlog(self):
        basepath = os.path.dirname(os.path.realpath(__file__))
        logdir = os.path.join(basepath, "./log")
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        self.logname = os.path.join(basepath, "./log/%s.log" % time.strftime("%Y%m%d%H"))
        LOG_FORMAT = '[%(asctime)s] : %(levelname)s %(filename)s - %(funcName)s(%(lineno)d) - %(message)s'
        logging.basicConfig(format=LOG_FORMAT, level=0, handlers=[logging.FileHandler(self.logname, 'a', 'utf-8')])

    def need_proxy(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))
            selfip = s.getsockname()[0]
        except Exception as e:
            logging.error(e)
            return False

        if selfip.startswith("192.168.") or selfip.startswith("10.")\
                or selfip.startswith("172.1") or selfip.startswith("10.64."):
            logging.debug("need proxy")
            return True
        else:
            logging.debug("no need proxy")
            return False

    def start(self, tgcli_port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            check = s.connect_ex(('127.0.0.1', tgcli_port))
            s.close()
        except Exception as e:
            logging.error(e)
            check = 1

        if check == 0:
            return True

        if self.need_proxy():
            cmd = """nohup proxychains telegram-cli --json --tcp-port %d >> %s 2>&1 &"""\
                % (tgcli_port, self.logname)
        else:
            cmd = """nohup telegram-cli --json --tcp-port %d >> %s 2>&1 &"""\
                % (tgcli_port, self.logname)

        logging.debug(cmd)
        ret = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        ret.wait()
        logging.debug("ret wait")
        reterr = ret.stderr.read()
        logging.debug("ret err")
        retout = ret.stdout.read()
        logging.debug("ret out")
        if reterr:
            logging.error(reterr.decode("utf8"))
            return False
        logging.info(retout)
        return True

    
    def parse_recive(self, msg_dict):
        logging.debug(msg_dict)

    def receive_loop(self):
        @coroutine
        def receive_coroutine_loop():
            while 1:
                msg = (yield)
                self.parse_recive(msg)
        self.receiver.start()
        self.receiver.message(receive_coroutine_loop())


    def get_channel_list(self, limit=0, offset=0):
        if limit == 0 and offset == 0:
            channels = self.sender.channel_list()
        else:
            channels = self.sender.channel_list(limit, offset)
        return channels

    def get_dialog_list(self, limit=0, offset=0):
        if limit == 0 and offset == 0:
            dialogs = self.sender.dialog_list()
        else:
            dialogs = self.sender.dialog_list(limit, offset)
        return dialogs

    def channel_get_members(self, name):
        members = self.sender.channel_get_members(name)
        return members

    def chat_get_members(self, name):
        chat_info_dict = self.sender.chat_info(name)
        meminfo_list = chat_info_dict["members"]
        return meminfo_list

    def get_history(self, peer, limit=0, offset=0):
        if limit == 0:
            ret = self.sender.history(peer, retry_connect=10, result_timeout=100)
        elif offset == 0:
            ret = self.sender.history(peer, limit, retry_connect=10)
        else:
            ret = self.sender.history(peer, limit, offset, retry_connect=10)
        #logging.debug(ret)
        ret.reverse()
        history_dict = collections.OrderedDict()
        for chat_info in ret:
            try:
                if chat_info["event"] != "message":
                    continue
                chatid = chat_info["id"]
                history_dict[chatid] = chat_info
                logging.debug(chat_info)
            except Exception as e:
                logging.error(e)
        return history_dict

    def create_group(self, groupname, userlist):
        try:
            ret = self.sender.create_group_chat(groupname, userlist[0])
            logging.debug(ret)
        except Exception as e:
            logging.error(e)
            return False

        if len(userlist) == 1:
            return True

        for username in userlist[1:]:
            try:
                ret = self.sender.chat_add_user(groupname, username, 0)
                logging.debug(ret)
            except Exception as e:
                logging.error(e)
        return True

