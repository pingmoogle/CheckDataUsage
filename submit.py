# -*- coding:UTF-8 -*-

import io
import json
import re
import sys
from urllib import parse

import requests
from PIL import Image


def main():
    rawdata = {}
    with open("rawdata.json","r") as rd:
        rawdata = json.load(rd)

    conn = requests.Session()

    ## Login

    result = conn.post("https://xxcapp.xidian.edu.cn/uc/wap/login/check",data={"username":rawdata["userID"],"password":rawdata["userPSWD"]})
    if result.status_code == 200:
        print("Login Done!\n")
    else:
        print("Login Failed.\nWrong UserID or Password.\n")

def showimage(URL):

    conn = requests.Session()
    pageres = conn.get(URL)
    
    img=Image.open(io.BytesIO(pageres.content))
    img.show()

    return input("Input the code: ")


def zfw():
    rawdata = {}
    with open("rawdata.json","r") as rd:
        rawdata = json.load(rd)
    useHeader = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
    }
    # Connect
    conn = requests.Session()
    pageres = conn.get("https://zfw.xidian.edu.cn/login", headers = useHeader)
    # Get Verify code
    #csrfdata = re.search('<meta name="csrf-token" content="(.*)">',pageres.text).group(1)
    csrfdata = re.search('<input type="hidden" name="_csrf" value="(.*)">		<div class="header">',pageres.text).group(1)
    #verifyimgURL = "https://zfw.xidian.edu.cn" + re.search('<img id="loginform-verifycode-image" src="(.*)" alt="">',pageres.text).group(1)
    #verify_code = showimage(verifyimgURL)
    # Post fromdata
    # result = conn.post("https://zfw.xidian.edu.cn",data={"_csrf":csrfdata,"LoginForm[username]":rawdata["userID"],"LoginForm[password]":rawdata["userPSWD"],"LoginForm[verifyCode]":verify_code,"login-button":NULL})
    #formdata = parse.quote("_csrf="+csrfdata+"&LoginForm[username]="+rawdata["userID"]+"&LoginForm[password]="+rawdata["userPSWD"]+"&LoginForm[verifyCode]"+verify_code+"&login-button=")
    #formdata = "_csrf="+ parse.quote(csrfdata) + "&LoginForm%5Busername%5D="+rawdata["userID"]+"&LoginForm%5Bpassword%5D="+rawdata["userPSWD"]+"&LoginForm%5BverifyCode%5D="+verify_code+"&login-button="
    formdata = {
        "_csrf":csrfdata,
        "LoginForm[username]":rawdata["userID"],
        "LoginForm[password]":rawdata["userPSWD"],
        # "LoginForm[verifyCode]":verify_code,
        # "login-button":""
        }
    
    # Return login result
    result = conn.post("https://zfw.xidian.edu.cn/login", data=formdata, headers = useHeader)
    try:
        pattern = re.compile(r'([0-9]+.?[0-9]*(byte|GB|MB))')
        dataLeft = pattern.findall(result.text)
    except AttributeError:
        print("Login filed!")
    else:
        print("每月免费10GB流量，已使用: " + str(dataLeft[0][0]))
        print("每月免费10GB流量，剩余: " + str(dataLeft[1][0]))
        print("充值流量已使用: " + str(dataLeft[2][0]))
        print("充值流量剩余: " + str(dataLeft[3][0]))
    
    conn.close()


if __name__ == "__main__":
    zfw()
