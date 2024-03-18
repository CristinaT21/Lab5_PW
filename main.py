import sys
import socket
import argparse


def make_http_request(url):
    host, port, path = parse_url(url)
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.encode())
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    return response.decode()


def parse_url(url):
    # Extract host, port, and path from URL
    url_parts = url.split("/")
    host_port = url_parts[2].split(":")
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 80
    path = "/" + "/".join(url_parts[3:])
    return host, port, path


def print_search_results(search_term):
    # Replace spaces with + for search query
    search_query = search_term.replace(" ", "+")
    response = make_http_request(f"https://www.google.com/search?q={search_query}")
    
    # Extract and print top 10 search results
    results = response.split("<h3 class=\"zBAuLc\"><a href=\"")[1:11]
    for i, result in enumerate(results):
        link = result.split("\"")[0]
        print(f"{i+1}. {link}")


def main():
    parser = argparse.ArgumentParser(description="CLI tool for making HTTP requests.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", dest="url", help="Make an HTTP request to the specified URL")
    group.add_argument("-s", dest="search_term", help="Make an HTTP request to search using the specified term")
    args = parser.parse_args()

    if args.url:
        response = make_http_request(args.url)
        print(response)
    elif args.search_term:
        print_search_results(args.search_term)


if __name__ == "__main__":
    main()
