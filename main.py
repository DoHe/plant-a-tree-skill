from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SkillHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        speech = not_understood()
        content_length = int(self.headers.get('content-length', 0))
        if content_length:
            try:
                body = self.rfile.read(content_length)
                parsed = json.loads(body)
                if parsed['request']['intent']['name'] == 'plant_tree':
                    number = parsed['request']['intent']['slots']['number'].get('value', None)
                    speech = plant_trees(number)
            except Exception as e:
                print(e)
        
        response = {
            "version": "1.0.0",
            "response": {
                "outputSpeech": speech,
                "shouldEndSession": True
            }

        }
        self.send_response(200, "All OK")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def not_understood():
    return {
        "type": "PlainText",
        "text": "I heard something about trees, that's awesome. But I didn't fully get you, can you repeat please?",
        "ssml": "<speak><p>I heard something about trees, that's awesome.</p><p>But I didn't fully get you, can you repeat please?</p></speak>"
    }


def plant_trees(number):
    if number is None:
        return {
            "type": "PlainText",
            "text": "I'll just go ahead and assume you want to plant just a single tree (which I now did). Thank you for saving the world!",
            "ssml": "<speak><p>I'll just do ahead and assume you want to plant just a <emphasis level=\"moderate\">single</emphasis> tree <break strength=\"weak\"/> (which I now did).</p><p>Thank you for saving the world!</p></speak>"
        }
    if int(number) <= 0:
        return {
            "type": "PlainText",
            "text": "You really have to plant more than zero trees to save the world...",
            "ssml": "<speak>You really have to plant more than zero trees to save the world...</speak>"
        }
    return {
        "type": "PlainText",
        "text": f"You just planted {number} trees. You rock!",
        "ssml": f"<speak><p>You just planted {number} trees.</p><p>You rock!</p></speak>"
    }


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