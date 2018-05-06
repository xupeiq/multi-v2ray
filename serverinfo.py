#! /usr/bin/env python
# -*- coding: utf-8 -*-

import readjson
import urllib2
import base64
import json

#判断传输配置
mystreamnetwork=str(readjson.ConfStreamNetwork)

if readjson.ConfStreamNetwork=="kcp" :
    if(readjson.ConfStreamHeader=="utp"):
        mystreamnetwork="mKCP 伪装 BT下载流量(utp)"
    elif(readjson.ConfStreamHeader=="srtp"):
        mystreamnetwork="mKCP 伪装 FaceTime通话(srtp)"
    elif(readjson.ConfStreamHeader=="wechat-video"):
        mystreamnetwork="mKCP 伪装 微信视频流量(wechat-video)"
    else:
        mystreamnetwork="mKCP"
elif readjson.ConfStreamNetwork=="http":
    mystreamnetwork="HTTP伪装"
elif readjson.ConfStreamNetwork=="ws":
    mystreamnetwork="WebSocket"
elif readjson.ConfStreamNetwork=="h2":
    mystreamnetwork="HTTP/2"

if (readjson.ConfStreamSecurity=="tls"):
    mystreamsecurity="TLS：开启\n"
    mystreamsecurity=mystreamsecurity + "伪装Path:%s" % str(readjson.ConfPath)
else:
    mystreamsecurity="TLS：关闭"

#输出信息
print("IP：%s") % str(readjson.ConfIP)
print("主端口：%s") % str(readjson.ConfPort)
print("UUID：%s") % str(readjson.ConfUUID)
print("alter ID: %s") % str(readjson.ConfAlterId)
print("传输方式：%s") % str(mystreamnetwork)
print("%s") % str(mystreamsecurity)
print("动态端口: %s") % str(readjson.ConfDyp)

#生成vmess字符串
jsonfile = file("/usr/local/v2ray.fun/json_template/vmess.json")
config = json.load(jsonfile)
config["add"]=str(readjson.ConfIP)
config["port"]=str(readjson.ConfPort)
config["id"]=str(readjson.ConfUUID)
config["aid"]=str(readjson.ConfAlterId)
config["net"]=str(readjson.ConfStreamNetwork)
if readjson.ConfStreamNetwork=="kcp":
    config["type"]=str(readjson.ConfStreamHeader)
if (readjson.ConfStreamSecurity=="tls"):
    config["tls"]="tls"
    config["host"]=str(readjson.ConfPath)
base64Str = base64.encodestring(json.dumps(config))
base64Str = ''.join(base64Str.split())
#绿色字体显示
print("\033[32m")
print("vmess://%s") % base64Str
print("\033[0m")