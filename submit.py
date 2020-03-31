# -*- coding:UTF-8 -*-

import requests, json, re, sys
import re
from PIL import Image
import io
from urllib import parse

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
    
    # Connect
    conn = requests.Session()
    use_headers = {
        "Content-Type": "text/html; charset = UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": "https://zfw.xidian.edu.cn/"
    }
    pageres = conn.get("https://zfw.xidian.edu.cn",headers = use_headers)
    # Get Verify code
    csrfdata = re.search('<meta name="csrf-token" content="(.*)">',pageres.text).group(1)
    verifyimgURL = "https://zfw.xidian.edu.cn" + re.search('<img id="loginform-verifycode-image" src="(.*)" alt="">',pageres.text).group(1)
    verify_code = showimage(verifyimgURL)
    # Post fromdata
    # result = conn.post("https://zfw.xidian.edu.cn",data={"_csrf":csrfdata,"LoginForm[username]":rawdata["userID"],"LoginForm[password]":rawdata["userPSWD"],"LoginForm[verifyCode]":verify_code,"login-button":NULL})
    # formdata = parse.quote("_csrf="+csrfdata+"&LoginForm[username]="+rawdata["userID"]+"&LoginForm[password]="+rawdata["userPSWD"]+"&LoginForm[verifyCode]"+verify_code+"&login-button=")
    formdata = {
        "_csrf":csrfdata,
        "LoginForm[username]":rawdata["userID"],
        "LoginForm[password]":rawdata["userPSWD"],
        "LoginForm[verifyCode]":verify_code,
        "login-button":""
        }
    
    # Return login result
    result = conn.post("https://zfw.xidian.edu.cn", data=formdata)
    try:
        dataLeft = re.search('<td data-col-seq="7">(.*)</td>',result.text).group(1)
    except AttributeError:
        print("Login filed!")
    else:
        print("剩余流量: " + dataLeft)
    
    conn.close()


if __name__ == "__main__":
    zfw()
