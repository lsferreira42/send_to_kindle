"""
Send my articles to kindle
"""
from time import sleep
from threading import Thread
import sys
import queue
import logging
import requests
from flask import Flask, request


app = Flask(__name__)

class UlrQueue:
    """
    Shared url queue
    """
    internal = queue.SimpleQueue()
    def put(self, value):
        """
        Put a value on the queue
        """
        if isinstance(value, dict):
            return self.internal.put_nowait(value)
        else:
            raise "Value must be a dict."

    def get(self):
        """
        Get a value from the queue
        """
        try:
            return self.internal.get_nowait()
        except:
            return False



def post_loop(urlqueue):
    """
    Loop and deploy
    """
    while True:
        try:
            url_dict = urlqueue.get()
            if url_dict:
                response = post_fivefilters(url_dict['url'])
                logging.info(response)
        except:
            sleep(1)
    return

def post_fivefilters(url):
    """
    Send the url to fivefilters service
    TODO: replace this to our scraping function
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.5,pt;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('context', 'send'),
        ('url', url),
    )

    data = [
        ('email', ''),
        ('email', 'leandrodsferreira_kindle'),
        ('from', ''),
        ('title', ''),
        ('domain', '2'),
        ('save', 'yes'),
    ]

    return requests.post('https://pushtokindle.fivefilters.org/send.php',
                         headers=headers,
                         params=params,
                         data=data
                        )

@app.route("/kindle", methods=["GET", "POST"])
def flask_main():
    """
    Main flask route
    """
    urlqueue = UlrQueue()
    response_body = """<html>
    <head>
    <script language=javascript>
    function closemyself() {
    window.opener=self;
    window.close();
    //self.close();
    }
    </script>
    <script language=javascript>
    function closemyself2() {
    open(location, '_self').close();
    }
    </script>
    <body onLoad="setTimeout('closemyself()',2000);">
    On queue!
    </body>
    </head>
    </html>"""
    url = request.args.get("url")
    urlqueue.put({"url": url})
    return response_body


def main():
    """
    Just main
    """
    urlqueue = UlrQueue()
    worker = Thread(target=post_loop, args=(urlqueue, ))
    worker.start()
    app.run(host="0.0.0.0", port=5003)
    return

if __name__ == "__main__":
    sys.exit(main())
