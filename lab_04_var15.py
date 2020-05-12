# py_ver == "3.6.9"
import flask


app = flask.Flask(__name__)


@app.route("/colour")
def set_colour():
    return """
            <html>
            <script>
            window.changeColour = function() {
            document.body.style.backgroundColor = location.hash.replace('#', '');
            document.getElementsByName("text")[0].innerHTML = decodeURI(location.hash.replace('#', ''));
            }
            </script>
            <body>
            <p name="text"></p>
            <div style="height:100vh" onmousemove=changeColour()></div>
            </body>
            </html>
            """


import cPickle, base64, hashlib


@app.route('/secret')
def get_msg():
    if flask.request.method == 'POST':
        if flask.request.data:
            msg = cPickle.loads(base64.b64decode(flask.request.data))
            if msg.hash == hashlib.sha256(msg.text.encode('utf8')).hexdigest():
                with open('messages', 'a') as msg_log:
                    msg_log.write(msg.text)


if __name__ == '__main__':
    app.run()
