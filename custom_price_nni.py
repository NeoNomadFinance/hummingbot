from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

price = "0.01"
UPDATE_INTERVAL = 2.0


hostName = "localhost"
serverPort = 2357


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global price

        try:
            response = requests.get("https://api.coingecko.com/api/v3/coins/neonomad-finance?market_data=true")
            result = response.json()
            new_price = result["market_data"]["current_price"]["usd"]
            price = new_price
        except Exception as e:
            print(f"Error occurred fetching price {e}. response: {response}")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(str(price), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
