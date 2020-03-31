# -*- coding:UTF-8 -*-

import io
import json
import re
import sys
from urllib import parse

import requests
from PIL import Image


def checkID():
    rawdata = {}
    with open("rawdata.json","r") as rd:
        rawdata = json.load(rd)

    conn = requests.Session()

    ## Login

    result = conn.post("https://xxcapp.xidian.edu.cn/uc/wap/login/check",data={"username":rawdata["userID"],"password":rawdata["userPSWD"]})
    if result.status_code == 200:
        logindata = {}
        logindata = json.loads(result.text)
        if logindata["m"] == "账号或密码错误":
            print("Login Failed.\nWrong UserID or Password.\n")
            sys.exit()
        else: pass
    else:
        print("Internet Connection Failed.")
        sys.exit()

def showimage(URL):

    conn = requests.Session()
    pageres = conn.get(URL)
    
    img=Image.open(io.BytesIO(pageres.content))
    img.show()

    return input("Input the code: ")


def main():
    rawdata = {}
    with open("rawdata.json","r") as rd:
        rawdata = json.load(rd)
    useHeader = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
    }
    # Check ID
    checkID()
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
        accountType = re.search(r'<span class="progress-text title-main">(.*)<\/span>',result.text).group(1)
        username = re.search(r'<label class="list-group-label">姓名<\/label>(.*)<\/li>',result.text).group(1)
        nextloopdate = re.search(r'<span class="package-value">(.*)<\/span>',result.text).group(1)
    except AttributeError:
        print("Login filed!")
    else:
        print("姓名: " + str(username))
        print("账户类型: " + str(accountType))
        print("每月免费10GB流量，已使用: " + str(dataLeft[0][0]))
        print("每月免费10GB流量，剩余: " + str(dataLeft[1][0]))
        print("下次免费流量重置日期: " + str(nextloopdate))
        print("充值流量已使用: " + str(dataLeft[2][0]))
        print("充值流量剩余: " + str(dataLeft[3][0]))
    
    conn.close()


if __name__ == "__main__":
    main()
