#!/usr/bin/env python
# coding: utf-8
from wxbot import *
import sqlite3
import os
import re


def create_table():
    conn.execute("create table msg (id integer primary key, msgid varchar(50), data varchar(300), name varchar(50), userid varchar(50), contype varchar(10))")
    
if os.path.exists('msg.db') == False:
    conn = sqlite3.connect('msg.db')
    cu=conn.cursor()
    create_table()

else:
    conn = sqlite3.connect('msg.db')
    cu=conn.cursor()

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        
        if msg['msg_type_id'] == 4 or msg['msg_type_id'] == 3:
            #ContentType
            #6是图片
            #4是语音
            #0是消息
            #10是撤回
            
            if msg['content']['type'] == 10:
                #print msg
                #print msg['content']['data']
                t = r'<msgid>(.*?)</msgid>'
                m =  re.findall(t,msg['content']['data'])
                #print m[0]
                cu.execute("select * from msg where msgid="+m[0])
                for row in cu:
                    print row
                    msgid = row[1]
                    data = row[2]
                    name = row[3]
                    userid = row[4]

                    contype = row[5]
                    
                    if contype == '6' or contype == '3':
                        self.get_msg_img(msgid)
                        self.send_msg_by_uid(u'['+name+u']刚刚撤回了:', userid)
                        self.send_img_msg_by_uid('temp/img_'+msgid+'.jpg', userid)
                        os.remove(('temp/img_'+msgid+'.jpg').encode("utf-8"))

                    if contype == '0':
                        self.send_msg_by_uid(u'['+name+u']刚刚撤回了:'+data, userid)
                    

                    break

            else:
                if msg['content']['type'] == 6 or msg['content']['type'] == 3 or msg['content']['type'] == 0:
                    #print msg
                    v = (msg['msg_id'], msg['content']['data'], msg['user']['name'], msg['user']['id'], msg['content']['type'])
                    cu.execute("insert into msg(msgid, data, name, userid, contype) values(?, ?, ?, ?, ?)", v)
                    conn.commit()

            
def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.is_big_contact = False   
    bot.run()


if __name__ == '__main__':
    
    main()
    #create_table()
