#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
import cookielib,urllib,urllib2
import imaplib, email


MAX_RETRY = 2

def main():
    c = noip()

    c.login()   
    if c.loginSucceed():
        print("login succeeded!")
        c.confirmHostname()
    else:
        print("login not succeeded!")


class noip: 

    #noipLogin = "https://www.noip.com/login"

    cookiejar = ""
    webSession = ""
    current_html = "" 

    def __init__(self):
        print("init called")
        self.cookiejar = cookielib.CookieJar()
        self.webSession = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

        self.userName = "USERNAME" # REPLACE
        self.userPass = "PASSWORD" # REPLACE

    def login(self):
        attempts = 0
        while attempts < MAX_RETRY:
            try:
                webResponse = self.webSession.open("https://www.noip.com/login")
                attempts = 99
            except urllib2.URLError as e:
                print(e.reason)
                attempts = attempts + 1
            except urllib2.HTTPError as e:
                print(e.reason)
                attempts = attempts + 1
        if attempts == MAX_RETRY:
            print("ERROR: connection failed - noip: ",sys.exc_info()[0])
            sys.exit("Error check logs")
        else:
            print("connection succeeded")
            html = webResponse.read()
            html = unicode(html,'utf-8')

        match = re.search(r'<input type="hidden" name="_token" value="(\w+)">',html)
        if match:
            chsm1 = match.group(1)
            dataForm = {"username" : self.userName, "password": self.userPass,"submit_login_page": "1", "_token": chsm1, "Login": "1", "submit_login_page": "1"}
        else:
            print("ERROR FOUND: change regular expression at login() for checksum. Probably No-IP changed web page structure")
            sys.exit("Error happens, check log.")

        dataPost = urllib.urlencode(dataForm)
        request = urllib2.Request("https://www.noip.com/login", dataPost)
        try:
            webResponse = self.webSession.open(request)
        except urllib2.HTTPError as e:
            print(e.reason)
            print(e.code)

        html = webResponse.read()
        current_html = unicode(html,'utf-8')



        if not 'noip_session' in [cookie.name for cookie in self.cookiejar]:
            print("Login error!: Incorrect No-IP User or password, please try again.")
    
    def loginSucceed(self):
        return 'noip_session' in [cookie.name for cookie in self.cookiejar]

    def confirmHostname(self):
        url="https://my.noip.com/api/host"
        request_headers = {
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest"
        }

        request = urllib2.Request(url,headers=request_headers)
        try:
            webResponse = self.webSession.open(request)
        except urllib2.HTTPError as e:
            print(url)
            print(e.reason)
            print(e.code)

        response = webResponse.read()
        json_data = json.loads(response)
        for i in json_data['hosts']:
            print i['id']
            url="https://my.noip.com/api/host/"+str(i['id'])+"/touch"
            request = urllib2.Request(url,headers=request_headers)
            try:
                webResponse = self.webSession.open(request)
            except urllib2.HTTPError as e:
                print(url)
                print(e.reason)
                print(e.code)

            response = webResponse.read()
            print(response)

main()

