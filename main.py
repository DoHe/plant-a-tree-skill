from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SkillHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        if content_length:
            body = self.rfile.read(content_length)
            parsed = json.loads(body)
            print(parsed)
        response = {
            "version": "1.0.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Your trees have been planted. Thank you for saving the world!",
                    "ssml": "<speak><p>Your trees have been planted.</p><p>Thank you for saving the world!</p></speak>"
                },
                "shouldEndSession": True
            }

        }
        self.send_response(200, "All OK")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        return


def main(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SkillHandler)
    print(f"Listening on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    import sys

    port = 8765
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    main(port)