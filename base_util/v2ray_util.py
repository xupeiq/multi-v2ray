#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import write_json
import random
import socket
import os
import re
from base_util import get_ssl
from base_util import tool_box

def choice_stream(new_stream_network, index_dict):
    if(new_stream_network==1):
        write_json.write_stream_network("tcp", "none", index_dict)
    elif(new_stream_network==2):
        print("请输入你想要为伪装的域名（不不不需要http）：")
        host=input()
        write_json.write_stream_network("tcp",str(host), index_dict)
    elif(new_stream_network==3):
        print("请输入你的服务器绑定域名（不不不需要http）：")
        host=input()
        write_json.write_stream_network("ws",str(host), index_dict)
    elif(new_stream_network==4):
        write_json.write_stream_network("mkcp","none", index_dict)
    elif(new_stream_network==5):
        write_json.write_stream_network("mkcp","kcp srtp", index_dict)
    elif(new_stream_network==6):
        write_json.write_stream_network("mkcp","kcp utp",index_dict)
    elif(new_stream_network==7):
        write_json.write_stream_network("mkcp","kcp wechat-video",index_dict)
    elif(new_stream_network==8):
        write_json.write_stream_network("mkcp","kcp dtls",index_dict)
    elif(new_stream_network==9):
        write_json.write_stream_network("h2","none", index_dict)

#随机一种 (srtp | wechat-video | utp) header伪装, 默认inbound组的主用户
def random_kcp(index_dict={'inboundOrDetour': 0, 'detourIndex': 0, 'clientIndex': 0, 'group': 'A'}):
    kcp_list=('mKCP + srtp', 'mKCP + utp', 'mKCP + wechat-video')
    choice = random.randint(5,7)
    print("随机一种 (srtp | wechat-video | utp) header伪装, 当前生成 %s" % kcp_list[choice - 5])
    print()
    choice_stream(choice, index_dict)

def change_tls(yn, index_dict):
    if yn == "on":
        print("\n请将您的域名解析到本VPS的IP地址，否则程序会出错！！\n")
        local_ip = tool_box.get_ip()
        print("本机器IP地址为：" + local_ip + "\n")
        input_domain=str(input("请输入您绑定的域名："))
        try:
            input_ip = socket.gethostbyname(input_domain)
        except Exception:
            print("\n域名检测错误!!!\n")
            return
        if input_ip != local_ip:
            print("\n输入的域名与本机ip不符!!!\n")
            return

        print("")
        print("正在获取SSL证书，请稍等。")
        get_ssl.getssl(input_domain)
        write_json.write_tls("on",input_domain, index_dict)
    elif yn == "off":
        write_json.write_tls("off","", index_dict)
        
    print("\n操作完成！\n")

def get_stats(type, meta_info, door_port, is_reset = False):
    is_reset = "true" if is_reset else "false"

    stats_cmd = "cd /usr/bin/v2ray && ./v2ctl api --server=127.0.0.1:%s StatsService.GetStats 'name: \"%s>>>%s>>>traffic>>>%s\" reset: %s'"
    type_tag = ("user" if type == 0 else "inbound")

    stats_real_cmd = stats_cmd % (str(door_port), type_tag, meta_info, "downlink", is_reset)
    downlink_result = os.popen(stats_real_cmd).readlines()
    if downlink_result and len(downlink_result) == 5:
        re_result = re.findall(r"\d+", downlink_result[2])
        if not re_result:
            print("当前无流量数据，请使用流量片刻再来查看统计!")
            return
        downlink_value = int(re_result[0])
        print("\033[36m")
        print("\ndownlink: " + tool_box.bytes_2_human_readable(downlink_value, 2) + "\n")

    stats_real_cmd = stats_cmd % (str(door_port), type_tag, meta_info, "uplink", is_reset)
    uplink_result = os.popen(stats_real_cmd).readlines()
    if uplink_result and len(uplink_result) == 5:
        re_result = re.findall(r"\d+", uplink_result[2])
        uplink_value = int(re_result[0])
        print("uplink: " + tool_box.bytes_2_human_readable(uplink_value, 2) + "\n")
        print("total: " + tool_box.bytes_2_human_readable(downlink_value + uplink_value, 2) + "\n")
        print("\033[0m")