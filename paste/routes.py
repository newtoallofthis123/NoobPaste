import json
from flask.wrappers import Request
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from paste.brain import debug_engine, add_to_db, undo, get_db, ran_quote, ran_joke, tinyurl, ran_fact, qr_code_engine
from flask.templating import render_template
from flask import request, make_response, jsonify
from paste import app
from paste.models import Bin

@app.route('/')
def paste():
    joke = ran_joke()
    author = "Hello " + str(request.cookies.get('author'))
    if author == "Hello None":
        return render_template('home.html', joke=joke)
    else:
        latest_url = str(request.cookies.get('latest_url'))
        return render_template('home.html', joke=joke, author=author, latest_url=latest_url)

@app.route('/create_temp', methods=["GET", "POST"])
def create_render():
    if request.method == "POST":
        language = request.form.get("language")
        return redirect(f'/create/{language}')

@app.route('/create/<lang>', methods=["GET", "POST"])
def create(lang):
    return render_template('search.html', language=lang, ran_quote=ran_quote())

@app.route('/paste/<hash>')
def paste_engine(hash):
    paste_info = get_db(hash)
    if paste_info == "No Such Paste":
        return render_template('404.html')
    else:
        url = "https://noobpaste.herokuapp.com/paste/" + paste_info.hash
        short_url = tinyurl(url)
        qr_code_engine(short_url)
        return render_template('paste.html', paste_info=paste_info, short_url=short_url, ran_fact=ran_fact())

@app.route('/done', methods=["GET", "POST"])
def done():
    if request.method == "POST":
        check = request.form.get("check")
        if check == "on":
            content = request.form.get("file_paste_content")
        else:
            content = request.form.get("paste_content")
        title = request.form.get("title")
        author = request.form.get("author")
        language = request.form.get("language")
        paste_info = add_to_db(title, content, author, language)
        url = "https://noobpaste.herokuapp.com/paste/" + paste_info["hash"]
        short_url = tinyurl(url)
        qr_code_engine(url)
        page_response = make_response(render_template('success.html', paste_info=paste_info, short_url=short_url))
        page_response.set_cookie('author', paste_info["author"])
        page_response.set_cookie('latest_url', paste_info["hash"])
        return page_response

@app.route('/api', methods=["POST"])
def api():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("paste_content")
        author = request.form.get("author")
        language = request.form.get("lang")
        paste_info = add_to_db(title, content, author, language)
        url = "https://noobpaste.herokuapp.com/paste/" + paste_info["hash"]
        short_url = tinyurl(url)
        paste_response = {
            "title": paste_info["title"],
            "author": paste_info["author"],
            "content": paste_info["content"],
            "lang": paste_info["lang"],
            "id": paste_info["hash"],
            "short_url": short_url
        }
        return jsonify(paste_response)
    else:
        return "Only POST requests allowed on this route, try /api/paste_id"

@app.route('/api/<hash>', methods=["GET"])
def get_api(hash):
    if request.method == "GET":
        paste_info = get_db(hash)
        if paste_info == "No Such Paste":
            return f'No Paste with Paste ID: {hash}'
        else:
            url = "https://noobpaste.herokuapp.com/paste/" + paste_info.hash
            short_url = tinyurl(url)
            paste_response = {
                "title": paste_info.title,
                "author": paste_info.author,
                "content": paste_info.content,
                "lang": paste_info.lang,
                "id": paste_info.hash,
                "short_url": short_url
            }
            return jsonify(paste_response)
    else:
        return "Only GET requests allowed on this route. Try /api"

@app.route('/license')
def license():
    return render_template('license.html')