from distutils.log import error
from paste.brain import *
from flask import request, make_response, jsonify, redirect, render_template, flash, get_flashed_messages
from paste import app, db, mail
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
from paste.models import Bin, User
from paste.forms import Register, Login
from flask_login import login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
import base64
import os
import hashlib

@app.route('/')
def paste():
    joke = ran_joke()
    author = str(request.cookies.get('author'))
    if request.cookies.get('username') != None:
        login = "true"
    else:
        login = "false"
    latest_url = str(request.cookies.get('latest_url'))
    return render_template('home.html', joke=joke, author=author, latest_url=latest_url, login=login)

@app.route('/about')
def about():
    api_content = "#API Implementation in Python\n\n#POST API\n\nimport requests\nimport json\n\nurl = 'https://noobpaste.herokuapp.com'\n\nparams={'title': 'title', 'paste_content': 'paste_content', 'author': 'author', 'lang': 'python', 'password': 'None'}\ndata = requests.post(f'{url}/post', params=params).content\njson_data = json.loads(data)\nprint(json_data)\n\n#get API\n\ndata = requests.get(f'{url}/api/<hash>/<password>'\njson_data = json.loads(data)\nprint(json_data)\n# By NoobScience 2022"
    return render_template('about.html', ran_fact=ran_fact(), api_content=api_content)

@app.route('/blog')
def blog():
    return render_template("blog.html", ran_quote=ran_quote())

@app.route('/blog/<blob>')
def blog_article(blob):
    return render_template(f'blog/{blob}.html', ran_quote=ran_quote())

@app.route('/<hash>')
def paste_shortcut(hash):
    paste_info = get_db(hash)
    if paste_info == "No Such Paste":
        return render_template('404.html')
    else:
        if paste_info.password == "None":
            url = "https://noobpaste.herokuapp.com/paste/" + paste_info.hash
            short_url = tinyurl(url)
            shortpaw_url = shortpaw(url)
            qr_code_engine(short_url)
            decrypted_content = decrypt(paste_info.content, paste_info.key)
            return render_template('paste.html', paste_info=paste_info, short_url=short_url, shortpaw=shortpaw_url, ran_fact=ran_fact(), content=decrypted_content)
        else:
            return redirect(f'/password/{hash}')

@app.route('/alt_login', methods=["get"])
def alt_login():
    if request.cookies.get('username') != None:
        user_info = login_engine(request.cookies.get('username'))
        if user_info is not None:
            login_user(user_info)
            flash(f'You are logged in as {request.cookies.get("username")}', category="success")
        else:
            flash(f'Error while logging you in as {request.cookies.get("username")}', category="danger")
        return "Logged In!"

@app.route('/code_edit_temp', methods=["GET", "POST"])
def code_edit_temp():
    lang = request.form.get("language")
    theme = request.form.get("theme")
    keybindings = request.form.get("keybindings")
    font = request.form.get("font")
    return redirect(f'/editor/lang={lang}&theme={theme}&keybindings={keybindings}&font="{font}"')

@app.route('/editor')
def code_edit():
    return render_template('code_edit.html')

@app.route('/editor/lang=<lang>&theme=<theme>&keybindings=<keybindings>&font=<font>', methods=["GET", "POST"])
def code_editor(lang, theme, keybindings, font):
    return render_template('code_editor.html', lang=lang, ran_quote=ran_quote(), hash=hash_gen_engine(), theme=theme, keybindings=keybindings, font=font)

@app.route('/md_editor')
def md_editor():
    return render_template("md_editor.html", ran_quote=ran_quote())

@app.route('/create_temp', methods=["GET", "POST"])
def create_render():
    if request.method == "POST":
        language = request.form.get("language")
        if language == "✨ Just Select a Language and Start Writing!":
            flash("Enter A Valid Language from the drop down", category="danger")
            return redirect(f'/')
        return redirect(f'/create/{language}')

@app.route('/create/<lang>', methods=["GET", "POST"])
def create(lang):
    return render_template('search.html', language=lang, ran_quote=ran_quote(), key=key_gen())

@app.route('/create')
def create_123():
    return redirect("/create/write")

@app.route('/password_check/<hash>', methods=["POST"])
def password_check(hash):
    password_to_check = request.form.get("password")
    paste_info = get_db(hash)
    if password_match_engine(paste_info.password, password_to_check):
            url = "https://noobpaste.herokuapp.com/paste/" + paste_info.hash
            short_url = tinyurl(url)
            shortpaw_url=shortpaw(url)
            qr_code_engine(short_url)
            decrypted_content = decrypt(paste_info.content, paste_info.key)
            return render_template('paste.html', paste_info=paste_info, short_url=short_url, shortpaw=shortpaw_url, ran_fact=ran_fact(), content=decrypted_content)
    else:
        return redirect(f'/password/{hash}')

@app.route('/password/<hash>')
def password(hash):
    paste_info = get_db(hash)
    if paste_info == "No Such Paste":
        return render_template('404.html')
    else:
        password = paste_info.password
        return render_template('password.html', password=password, hash=hash)

@app.route('/password_edit_check/<hash>', methods=["POST"])
def password_edit_check(hash):
    password_to_check = request.form.get("password")
    paste_info = get_db(hash)
    if password_match_engine(paste_info.password, password_to_check):
            decrypted_content = decrypt(paste_info.content, paste_info.key)
            return render_template('paste_edit.html', paste_info=paste_info, ran_quote=ran_quote(), content=decrypted_content)
    else:
        return redirect(f'/password_edit/{hash}')

@app.route('/password_edit/<hash>')
def password_edit(hash):
    paste_info = get_db(hash)
    if paste_info == "No Such Paste":
        return render_template('404.html')
    else:
        password = paste_info.password
        return render_template('password_edit.html', password=password, hash=hash)

@app.route('/edit_done', methods=["GET", "POST"])
def edit_done():
    if request.method == "POST":
        content = censor(request.form.get("paste_content"))
        password = hash_engine(request.form.get("password"))
        title = request.form.get("title")
        author = request.form.get("author")
        language = request.form.get("language")
        hash = request.form.get("hash")
        paste_info = edit_db(author=author, title=title, language=language, password=password, content=content, hash=hash)
        url = "https://noobpaste.herokuapp.com/paste/" + paste_info["hash"]
        short_url = tinyurl(url)
        shortpaw_url = shortpaw(url)
        decrypted_content = decrypt(paste_info["content"], paste_info["key"])
        page_response = make_response(render_template('success.html', paste_info=paste_info, short_url=short_url, shortpaw=shortpaw_url, ran_fact=ran_fact(), content=decrypted_content))
        page_response.set_cookie('author', paste_info["author"])
        page_response.set_cookie('latest_url', paste_info["hash"])
        page_response.set_cookie('time', time_cal())
        return page_response

@app.route('/edit/<hash>')
def edit(hash):
    paste_info = get_db(hash)
    if paste_info == "No Such Paste":
        return render_template('404.html')
    else:
        if paste_info.password == "None":
            url = "https://noobpaste.herokuapp.com/paste/" + paste_info.hash
            decrypted_content = decrypt(paste_info.content, paste_info.key)
            return render_template('paste_edit.html', paste_info=paste_info, ran_quote=ran_quote(), content=decrypted_content)
        else:
            return redirect(f'/password_edit/{hash}')    

@app.route('/delete/<hash>')
def delete(hash):
    paste_info = del_db(hash)
    if paste_info == "No Such Paste":
        return redirect('/404')
    else:
        flash(f'Deleted Paste with hash: {hash}')
        return redirect('/')

@app.route('/paste/<hash>')
def paste_engine(hash):
    paste_info = get_db(hash)
    if paste_info == "No Such Paste":
        return render_template('404.html')
    else:
        if paste_info.password == "None":
            url = "https://noobpaste.herokuapp.com/paste/" + paste_info.hash
            short_url = tinyurl(url)
            shortpaw_url = shortpaw(url)
            qr_code_engine(short_url)
            decrypted_content = decrypt(paste_info.content, paste_info.key)
            return render_template('paste.html', paste_info=paste_info, short_url=short_url, shortpaw=shortpaw_url, ran_fact=ran_fact(), content=decrypted_content)
        else:
            return redirect(f'/password/{hash}')

@app.route('/done', methods=["GET", "POST"])
def done():
    if request.method == "POST":
        check = request.form.get("check")
        if check == "on":
            content = censor(request.form.get("file_paste_content"))
        else:
            content = censor(request.form.get("paste_content"))
        password_check = request.form.get("password_check")
        if password_check == "on":
            password = hash_engine(request.form.get("password"))
        else:
            password = "None"
        custom_check = request.form.get("custom_check")
        title = request.form.get("title")
        author = request.form.get("author")
        language = request.form.get("language")
        if custom_check == "on":
            custom_hash = request.form.get("custom_hash")
            paste_info = custom_add_to_db(title=title, content=content, author=author, lang=language, custom_hash=custom_hash, password=password)
        else:
            paste_info = add_to_db(title, content, author, language, password)
        url = "https://noobpaste.herokuapp.com/paste/" + paste_info["hash"]
        short_url = tinyurl(url)
        shortpaw_url = shortpaw(url)
        qr_code_engine(url)
        decrypted_content = decrypt(paste_info["content"], paste_info["key"])
        page_response = make_response(render_template('success.html', paste_info=paste_info, short_url=short_url, shortpaw=shortpaw_url, ran_fact=ran_fact(), content=decrypted_content))
        page_response.set_cookie('author', paste_info["author"])
        page_response.set_cookie('latest_url', paste_info["hash"])
        page_response.set_cookie('time', time_cal())
        return page_response

@app.route('/register', methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        password_hashed = hash_engine(form.password.data)
        user_1 = User(username=form.username.data, email=form.email.data, password_hashed=password_hashed, time=time_cal())
        db.session.add(user_1)
        db.session.commit()
        login_user(user_1)
        welcome_mail(form.username.data)
        register_response = make_response(redirect('/'))
        register_response.set_cookie('username', form.username.data)
        register_response.set_cookie('password', form.password.data)
        return register_response
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error while creating user: {error_msg}')
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        hashed_password = hash_engine(form.password.data)
        user_info = login_engine(form.username.data)
        if user_info is not None:
            if password_match_engine(user_info.password_hashed, form.password.data):
                login_user(user_info)
                flash(f'You are logged in as {form.username.data}', category="success")
                login_response = make_response(redirect('/'))
                login_response.set_cookie('username', form.username.data)
                login_response.set_cookie('password', user_info.password_hashed)
                return login_response
            else:
                flash(f'Check your Password and try again', category="danger")
        else:
            flash(f'Error while logging you in as {form.username.data}', category="danger")
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error while logging in user: {error_msg}', category="danger")
    return render_template('login.html', form=form)

@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    logout_user()
    form = Login()
    if form.validate_on_submit():
        hashed_password = hash_engine(form.password.data)
        user_info = login_engine(form.username.data)
        if user_info is not None:
            if password_match_engine(user_info.password_hashed, form.password.data):
                if user_info.username == "noobscience123":
                    login_user(user_info)
                    flash(f'You are logged in as {form.username.data}', category="success")
                    login_response = make_response(redirect('/admin'))
                    return login_response
                else:
                    return redirect('/login')
            else:
                flash(f'Check your Password and try again', category="danger")
        else:
            flash(f'Error while logging you in as {form.username.data}', category="danger")
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There was an error while logging in user: {error_msg}', category="danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def log_out():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect('/')

@app.route('/authors/<author>')
def author(author):
    author_posts = get_db_author(author)
    if author_posts is not None:
        return render_template('author.html', author=author, posts=author_posts)
    else:
        return f'You have not created any pastes: click <a href="/create/write">here</a> to get started'

@app.route('/otp', methods=["post"])
def otp_gen():
    email = request.values.get("email")
    otp = otp_gen_engine()
    otp_mail = Message('Confirm OTP to Register for NoobPaste', sender = 'noobsciencesmtp@gmail.com', recipients = [email])
    otp_mail.html = '<div style="text-align: center;"><img src="https://github.com/newtoallofthis123/Assets/raw/main/Image/noobscience.png" style="width: 54px; height: 54px;" alt="NoobPaste Image"><h2>NoobPaste Registration</h2><p>Hey! Did you by any chance try to register with <a href="https://noobpaste.herokuapp.com">NoobPaste</a>? If so, this is your otp</p><h2 style="text-align: center; font-family: Courier, monospace">' +  otp + '</h2><p>Ignore if this was not done by you</p></div>'
    mail.send(otp_mail)
    flash("OTP Sent to Email", category="info")
    return otp

@app.route('/email', methods=["post"])
def email():
    username = request.values.get("username")
    email_info = get_email(username)
    if email_info == "No Such User":
        return "No Such User"
    else:
        email = email_info.email
        return jsonify(email)

@app.route('/send_email', methods=["post"])
@cross_origin(supports_credentials=True)
def send_email():
    email = request.values.get("email")
    name = request.values.get("name")
    content = request.values.get("content")
    send_email = email_send(email=email, name=name, content=content)
    return "Done"

@app.route('/subscribe_news_letter', methods=["post"])
@cross_origin(supports_credentials=True)
def subscribe_news_letter():
    email = request.values.get("email")
    news_letter_info = news_letter(email)
    return "Done"

@app.route('/send_news_letter', methods=["post"])
@cross_origin(supports_credentials=True)
def news_letter():
    title = request.values.get("title")
    content = request.values.get("content")
    news_letter = send_news_letter(title, content)
    return "Done"

@app.route('/dino', methods=["get", "post", "put", "delete"])
def dino():
    if request.method == "GET":
        hash = str(request.values.get("hash"))
        if hash == None:
            return jsonify("Okay! You do know Dino 🤖 needs the [hash] to give you the paste content!")
        else:
            paste_content = get_db(hash)
            if paste_content == "No Such Paste":
                return jsonify(f'No Such Paste with hash: {hash} found.')
            else:
                content = decrypt(paste_content.content, paste_content.key)
                response = {
                    "status_code" : 200,
                    "service": "NoobPaste Dino API v.2.1",
                    "hash": hash,
                    "authentication_through": paste_content.author,
                    "response": {
                        "title": paste_content.title,
                        "author": paste_content.author,
                        "paste_content": {
                            "lang": paste_content.lang,
                            "content": content,
                            "time_modified": paste_content.time,
                        }
                    },
                    "time_of_request": time_cal(),
                    "encryption": "Content Decrypted through key stored in database.",
                    "url": f'https://noobpaste.herokuapp.com/{hash}',
                    "short_url": tinyurl(f'https://noobpaste.herokuapp.com/{hash}'),
                }
                print(paste_content.password)
                if paste_content.password == "None":
                    return jsonify(response)
                else:
                    password = str(request.values.get("password"))
                    if password == None:
                        return jsonify("The paste is protected by password. Enter the password as a parameter and try again")
                    else:
                        print(password_match_engine(paste_content.password, password))
                        if password_match_engine(paste_content.password, password):
                            return jsonify(response)
                        else:
                            return jsonify("The paste is protected by password. Enter the Correct password as a parameter and try again")
    if request.method == "POST":
        title = request.values.get("title")
        if title == None:
            return jsonify("Send in a valid title")
        author = request.values.get("author")
        if author == None:
            author = "Anon"
        password = request.values.get("password")
        if password == None:
            password = "None"
        content = request.values.get("content")
        if content == None:
            return jsonify("Send in valid content to store")
        lang = request.values.get("lang")
        if lang == None:
            return jsonify("Send in a valid Language")
        paste_content = add_to_db(title=title, content=content, author=author, lang=lang, password=password)
        content = decrypt(paste_content["content"], paste_content["key"])
        response = {
            "status_code" : 200,
            "service": "NoobPaste Dino API v.2.1",
            "hash": paste_content["hash"],
            "authentication_through": paste_content["author"],
            "response": {
                "title": paste_content["title"],
                "author": paste_content["author"],
                "paste_content": {
                    "lang": paste_content["lang"],
                    "content": content,
                    "time_modified": time_cal(),
                }
            },
            "time_of_request": time_cal(),
            "encryption": "Content Decrypted through key stored in database.",
            "url": f'https://noobpaste.herokuapp.com/{paste_content["hash"]}',
            "short_url": tinyurl(f'https://noobpaste.herokuapp.com/{paste_content["hash"]}'),
        }
        return jsonify(response)
    if request.method == "PUT":
        hash = str(request.values.get("hash"))
        if hash == None:
            return jsonify("Okay! You do know Dino 🤖 needs the [hash] to give you the paste content!")
        else:
            paste_content = get_db(hash)
            if paste_content == "No Such Paste":
                return jsonify(f'No Paste with hash: {hash} found.')
            else:
                paste_content_1 = decrypt(paste_content.content, paste_content.key)
                title = request.values.get("title")
                if title == None:
                    title = paste_content.title
                author = request.values.get("author")
                if author == None:
                    author = paste_content.author
                password = request.values.get("password")
                if password == None:
                    password = paste_content.password
                content = request.values.get("content")
                if content == None:
                    content = paste_content_1
                lang = request.values.get("lang")
                if lang == None:
                    lang = paste_content.lang
                paste_edited = edit_db(author=author, title=title, content=paste_content_1, language=lang, password=password, hash=paste_content.hash)
                response = {
                    "status_code" : 200,
                    "service": "NoobPaste Dino API v.2.1",
                    "hash": paste_edited["hash"],
                    "authentication_through": paste_edited["author"],
                    "response": {
                        "title": paste_edited["title"],
                        "author": paste_edited["author"],
                        "paste_content": {
                            "lang": paste_edited["lang"],
                            "content": content,
                            "time_modified": time_cal(),
                        }
                    },
                    "time_of_request": time_cal(),
                    "encryption": "Content Decrypted through key stored in database.",
                    "url": f'https://noobpaste.herokuapp.com/{paste_edited["hash"]}',
                    "short_url": tinyurl(f'https://noobpaste.herokuapp.com/{paste_edited["hash"]}'),
                }
                return jsonify(response)
    if request.method == "DELETE":
        hash = str(request.values.get("hash"))
        if hash == None:
            return jsonify("Okay! You do know Dino 🤖 needs the [hash] to give you the paste content!")
        else:
            paste_content = del_db(hash)
            if paste_content == "No Such Paste":
                return jsonify(f'Deleted Paste with hash: {hash}')
            else:
                return jsonify(f'Successfully Deleted Paste with hash: {hash}')
    else:
        return jsonify("NoobPaste Dino API 🤖 v.2.1: For Full Docs: /docs")

@app.route('/docs')
def docs():
    return render_template('docs.html', ran_quote=ran_quote())

@app.post('/gravatar')
def gravatar():
    email = request.values.get("email")
    gravatar_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    gravatar_url = jsonify({"src": f'https://www.gravatar.com/avatar/{gravatar_hash}'})
    return gravatar_url

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html", error_code=404)

@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template("error.html", error_code=405)

@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", error_code=500)

@app.route('/license')
def license():
    return render_template('license.html')
