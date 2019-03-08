from flask import Flask, request
import requests
import sys

DEBUG = True
app = Flask(__name__)

# TODO: make threaded
# TODO: use queue

def post_fivefilters(url):
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

  return requests.post('https://pushtokindle.fivefilters.org/send.php', headers=headers, params=params, data=data)

def debug(response):
    if DEBUG:
        return str(response)
    return ""

@app.route("/kindle", methods=["GET", "POST"])
def flask_main():
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
"""
    url = request.args.get("url")
    response = post_fivefilters(url)
    response_body += "URL: {}<br>Status Code: {}<br>Debug Info: <br>{}".format(
        url,
        response.status_code,
        debug(response))
    response_body += """    </body>
  </head>
</html>"""
    return response_body


def main():
    url = sys.argv[1]
    if url == "api":
        app.run(host="0.0.0.0", port=5003)
        return
    response = post_fivefilters(url)
    print("Status Code: {}\nDebug Info: \n{}".format(
        response.status_code,
        debug(response)))
    return

if __name__ == "__main__":
    sys.exit(main())