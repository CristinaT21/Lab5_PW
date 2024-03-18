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

def parse_url(url):
    # Extract host, port, and path from URL
    url_parts = url.split("/")
    host_port = url_parts[2].split(":")
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 80
    path = "/" + "/".join(url_parts[3:])
    return host, port, path

def make_http_request(url, use_cache=True):
    host, port, path = parse_url(url)
    request = f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, 80))
            client_socket.sendall(request.encode("utf-8"))
            response = b''
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data

            client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    content_type = ""
    for header in response.split(b'\r\n'):
        if header.startswith(b'Content-Type:'):
            content_type = header.decode().split(': ')[1]
            break

    if "application/json" in content_type:
        return json.loads(response.split(b'\r\n\r\n')[1])

    return response

def return_search_results(response):
    soup = BeautifulSoup(response, 'html.parser')
    print("\nSearch Results:")
    results = soup.find_all('li', class_='b_algo')
    for i, result in enumerate(results[:10]):
        print(f"{i+1}. {result.h2.get_text()}")
        link = result.find('cite')
        print(f"   {link.get_text()}")
        description = result.find('p')
        print(f"   {description.get_text()}\n")
    return

def print_error():
    print("Invalid arguments. Use 'go2web -h' for help.")
    return

def main():
    if sys.argv[1] == "-s":
        if len(sys.argv) == 3:
            search_term = sys.argv[2]
            search_term = search_term.replace(" ", "+")
            print(f"Searching for: {search_term}")
            results = make_http_request(f"https://www.bing.com/search?q={search_term}")
            return_search_results(results)
        else:
            print_error()
            return
    elif sys.argv[1] == "-h":
        print("Help:\n\
                go2web -u <URL>         # make an HTTP request to the specified URL and print the response\n\
                go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results \n\
                go2web -h               # show this help \n")
        return

if name == "main":
    main()
