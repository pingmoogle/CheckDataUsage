# -*- coding: UTF-8 -*-

import json


def AskBoolean(tips):
    ans = input(tips + "<Y/N> ").upper()
    if ans == "Y":
        return 1
    if ans == "N":
        return 0


if __name__ == '__main__':
    rawdata = {}

    rawdata.update({"userID": input("Enter your ID: ")})
    rawdata.update({"userPSWD": input("Enter your Password: ")})
    # rawdata.update({"sfzx":AskBoolean("Have you been in Hubei today?")})

    print("Your info is as followed:")
    print(rawdata)

    with open("rawdata.json", "w") as fileLink:
        try:
            json.dump(rawdata, fileLink)
        except IOError:
            print("IO error.")
        else:
            print("Done!")
