#!/usr/bin/python3

import requests
import threading
from bs4 import BeautifulSoup

words = []


url = input("Enter a valid url:- ")
recursive = True

try:
    page = requests.get(url)
except:
    print("Invalid Url")
    exit()

if url[-1] != "/":
    url = url + "/"


# http://13.126.7.62/

with open("./wordlists/big.txt") as f:
    print("getting wordslist")
    for line in f.readlines():
        try:
            newPage = requests.get(url+line.strip("\n"))
            print("Got endpoint /"+line.strip("\n"))
            endpointFile = open("./endpoints.txt", 'a')
            endpointFile.write(url+line)
            endpointFile.close()
            print(url+line.strip("\n"))
        except KeyboardInterrupt:
            break
        except:
            print(line.strip("\n") + "  Failed")
