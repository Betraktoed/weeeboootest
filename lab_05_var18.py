# py_ver == "3.6.9"
import flask
import requests
import xml
import defusedxml
import xml.dom.minidom


app = flask.Flask(__name__)


# root_ssh_pwd = "k33pc41mU$$Ri$c0min9"
# main_server_ip = "8.8.8.8"

@app.errorhandler(404)
def page_not_found(error):
    d = {"<": "&#x3C;", ">": "&#x3E;", '"': "&#x22;"}

    url = flask.request.path
    url_word = []
    for word in url:
        if word in d:
            url_word.append(d[word])
        else:
            url_word.append(word)
    new_url = ''.join(url_word)

    return """
          <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
          <title>404 Not Found</title>
          <h1>Not Found</h1>
          <p>The requested path <b>%s</b> was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
          """ % new_url


@app.route('/parser', methods=['GET', 'POST'])
def parse_list():
    if flask.request.method == 'POST':
        if 'file' not in flask.request.files:
            return flask.redirect(flask.request.url)
        file = flask.request.files['file']
        if file.filename == '':
            return flask.redirect(flask.request.url)
        if file and file.filename.endswith(".xml"):
            from xml.dom import pulldom
            parser = pulldom.parse(file)
            for node in parser:
                data = node[1]
                parser.expandNode(data)
                requests.post("https://storage.mainfraim.ecc/save_data", data=data.toxml())
    return flask.redirect('/load_xml')


@app.route('/load_xml')
def loader():
    return """
    <html>
      <body>
        <h2>Загрузите XML-документ для обработки</h2>
        <form action="/parser" method="post" enctype="multipart/form-data">
          <input name="file" type="file">
          <input name="submit" type="submit" value="Загрузить">
        </form>
      </body>
    </html>
    """


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Security-Policy'] = "default-src 'self'"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    app.run()
