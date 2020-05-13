# py_ver == "3.6.9"
import flask

import cgi;
app = flask.Flask(__name__)


@app.route('/introduction')
def introduction():
    return """
            <html>
                <title>Знакомство</title>
                <body>
                    <form action="/set_name">
                        Представьтесь, пожалуйста: <input name="name" type="text" />
                        <input name="submit" type="submit">
                    </form>
                </body>
            </html>
"""


@app.route('/')
def index_page():
    if flask.request.cookies.get('name'):
        return """
            <html>
                <title>Приветствие</title>
                <body>
		<h1>Привет, %s!</h1>
                </body>
            </html>
"""% cgi.escape(flask.request.cookies.get('name'))
    else:
        return """
            <html>
                <title>Приветствие</title>
                <script></script>
                <body>
                    <a href="/introduction">Как вас зовут?</a>
                </body>
            </html>
"""


@app.route('/set_name')
def cookie_setter():
    response = flask.make_response(flask.redirect('/'))
    max_age = 60*60*24*7
    response.set_cookie('name', flask.request.args.get('name'),max_age,secure=True,httponly=True,samesite='Strict')
    return response


import requests
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


if __name__ == '__main__':
    app.run()
