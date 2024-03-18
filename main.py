#!/usr/bin/python3
import sys
import time
import socket
import ssl
import json
from ssl import SSLContext
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

def main():
    if sys.argv[1] == "-h":
        print("Help:\n\
                go2web -u <URL>         # make an HTTP request to the specified URL and print the response\n\
                go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results \n\
                go2web -h               # show this help \n")
        return

if name == "main":
    main()
