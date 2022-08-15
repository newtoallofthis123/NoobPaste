import base64
from paste.models import Bin, User, News_letter
import random
import string
from datetime import datetime, date
from paste import app, db, bcrypt, mail
import json
import requests
from flask_mail import Mail, Message
import pyjokes
from base64 import b64encode, b64decode
import hashlib
import os
from cryptography.fernet import Fernet


def hash_gen_engine():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    whole =  lower + upper + digits
    hash_string = random.sample(whole, 8)
    hash = "".join(hash_string)
    return hash

def otp_gen_engine():
    digits = string.digits
    whole =  digits
    otp_string = random.sample(whole, 6)
    otp = "".join(otp_string)
    return otp

def censor(content):
    import re
    censor_node = re.compile('([Ff][Uu]*[Cc]*[Kk]|[Ss]+[Ee]+[Xx]|[Dd]+[Ii]*[Cc]*[Kk]|[Pp][Us][Us][Yy]|[Pp][Oo]+[Rr]+[Nn])')
    censored = censor_node.sub("*CENSORED*", content)
    return censored 

def time_cal():
    current_t = datetime.now()
    current_date = str(date.today())
    current_t_f = current_t.strftime("%H:%M:%S")
    timeAnddate = (f'{current_t_f} {current_date}')
    return timeAnddate

def add_to_db(title, content, author, lang, password):
    hash = hash_gen_engine()
    key = Fernet.generate_key().decode()
    time = time_cal()
    content = encrypt(content, key).decode()
    paste_info = Bin(title=title, hash=hash, content=content, lang=lang, key=key, author=author, time=time, password=password)
    db.session.add(paste_info)
    db.session.commit()
    db.session.refresh(paste_info)
    paste_info = {"title": title, "hash": hash, "content": content, "lang": lang, "key": key, "author": author, "password": password}
    return paste_info

def welcome_mail(username):
    user = User.query.filter_by(username=username).first()
    welcome_mail = Message('Welcome to NoobPaste', sender = 'noobsciencesmtp@gmail.com', recipients = [user.email])
    welcome_mail.html = '<div style="text-align: center;"><img src="https://github.com/newtoallofthis123/Assets/raw/main/Image/noobscience.png" style="width: 54px; height: 54px;" alt="NoobPaste Image"><h2>Welcome! To NoobPaste</h2><p>Hey' + user.username + '! You have successfully registered with <a href="https://noobpaste.herokuapp.com">NoobPaste</a>. NoobPaste is an awesome tool that can easily be implemenented into your workflow. Share and get code easily with high efficiency and never have to use anothe pastebin. NoobPaste is opensource and you can host it on your own! <a href="https://github.com/newtoallofthis123/NoobPaste">Source Code</a>.</p><h2>Summary of NoobPaste Build and Use</h2><p>NoobPaste is written in python using the flask micro framework. It is very fast and is very secure. NoobPaste uses a database to store your data. Even if you donot set a password, your data is encrypted with a key. The data is acessed using postgregsql. This setup should be relatively safe. Your Code is stored in a database which is queried everytime you make a request. Unless you have the exact 8 character string, accidentally stubling onto another code is quite rare. Password Protection Available. NoobPaste is deployed on heroku. Heroku servers take some time to activate but once they do, they are relatively fast. NoobPaste is simply meant to act as a good alternative to pastebin and it is till in beta. So, use it with care and do not post anything sensitive on it.</p><button style="padding: 12px;"><a style="text-decoration: none;" href="https://noobpaste.herokuapp.com">Start Now!</a></button><h2 style="text-align: center; font-family: Courier, monospace">Enjoy NoobPaste!</h2><p>Author,</p><a href="https://newtoallofthis123.github.io/About">NoobScience</a></div>'
    mail.send(welcome_mail)

def email_send(name, email, content):
    email_send = Message(f'✉ {name} sent you a new mail!', sender = 'noobsciencesmtp@gmail.com', recipients = ['noobscience123@gmail.com'])
    email_send.html = '<div style="text-align: center;"><style>h1{font-family: Calibri, sans-serif;font-size: 42px;}p{font-family: sans-serif;font-weight: 300;font-size: 18px;}h2{font-family: sans-serif;font-size: 28px;}a{text-decoration: none;transition-delay: 50ms;transition-duration: 1s;}</style><img src="https://github.com/newtoallofthis123/Assets/raw/main/Image/noobscience.png" style="width: 54px; height: 54px;" alt="NoobPaste Image"><h1>' + name + ' sent you a mail!</h1><p>' + content + '</p><h2>This was sent by <a href="mailto:' + email + '">' + email + '</a></h2></div>'
    mail.send(email_send)

def get_email(username):
    content = User.query.filter_by(username=username).first()
    if content == None:
        return "No Such User"
    else:
        return content

def get_db(hash):
    content = Bin.query.filter_by(hash=hash).first()
    if content == None:
        return "No Such Paste"
    else:
        return content

def edit_db(author, title, password, content, language, hash):
    paste_content = Bin.query.filter_by(hash=hash).first()
    paste_content.author = author
    paste_content.password = password
    paste_content.title = title
    paste_content.content = encrypt(content, paste_content.key).decode()
    encrypted_content = encrypt(content, paste_content.key).decode()
    paste_content.language = language
    db.session.add(paste_content)
    db.session.commit()
    db.session.refresh(paste_content)
    paste_info_content = {"title": title, "hash": hash, "content": encrypted_content, "lang": language, "key": paste_content.key, "author": author, "password": password}
    return paste_info_content

def del_db(hash):
    content = Bin.query.filter_by(hash=hash).first()
    if content == None:
        return "No Such Paste"
    else:
        Bin.query.filter_by(hash=hash).delete()
        db.session.commit()
        return "Deleted Entry"

def news_letter(email):
    time = time_cal()
    news_letter_info = News_letter(email=email, time=time)
    db.session.add(news_letter_info)
    db.session.commit()
    db.session.refresh(news_letter_info)

def send_news_letter(title, content):
    emails = News_letter.query.all()
    mail_list = []
    for email in emails:
        mail_list.append(email.email)
    email_send = Message(f'{title}', sender = 'noobsciencesmtp@gmail.com', recipients = mail_list)
    email_send.html = content
    mail.send(email_send)

def get_db_author(author):
    content = Bin.query.filter_by(author=author).all()
    return content

def debug_engine():
    debug_content = User.query.all()
    return debug_content

def undo():
    db.session.rollback()

def ran_quote():
    try:
        quotes_page = json.loads(requests.get("https://api.quotable.io/random").content)
        quote_list = [quotes_page["content"], quotes_page["author"]]
        return quote_list
    except:
        quote_list = ["Never give up!", "EveryOne in The World!"]

def ran_joke():
    joke = pyjokes.get_joke(category="neutral")
    return joke

def ran_fact():
    fact_page = json.loads(requests.get("https://useless-facts.sameerkumar.website/api").content)
    fact = fact_page["data"]
    return fact

def tinyurl(url):
    tinyurl_page = str(requests.get(f'https://tinyurl.com/api-create.php?url={url}').content).replace("b'", "").replace("'", "")
    return tinyurl_page

def shortpaw(url):
    data = {"url": url}
    shortpaw_page = json.loads(requests.post(f'https://shortpaw.herokuapp.com/api', params=data).content)
    return f'https://shortpaw.herokuapp.com/{shortpaw_page["hash"]}'

def qr_code_engine(url):
    import pyqrcode
    qr_code = pyqrcode.create(url)
    qr_code.svg('paste/static/assets/images/qr_code.svg', background="white", scale=8)

def hash_engine(password):
    password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    return password_hashed

def login_engine(username):
    username_details = User.query.filter_by(username=username).first()
    return username_details

def password_match_engine(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)

def check_hash_duplicate(hash):
    hash_check = Bin.query.filter_by(hash=hash).first()
    if hash_check:
        return hash_gen_engine()
    else:
        return hash

def custom_add_to_db(title, content, author, lang, custom_hash, password):
    hash = check_hash_duplicate(custom_hash)
    key = Fernet.generate_key().decode()
    time = time_cal()
    content = encrypt(content, key)
    paste_info = Bin(title=title, hash=hash, content=content, lang=lang, key=key, author=author, time=time, password=password)
    db.session.add(paste_info)
    db.session.commit()
    paste_info = {"title": title, "hash": hash, "content": content, "lang": lang, "key": key, "author": author, "password": password}
    return paste_info

# Please help Me!

def key_gen():
    key = Fernet.generate_key()
    return key

def encrypt(content, key):
    fernet = Fernet(key)
    encrypted_content = fernet.encrypt(content.encode())
    return encrypted_content

def decrypt(content, key):
    # print(bytes(key, encoding='utf8').decode())
    fernet = Fernet(key.encode())
    decrypted_content = (fernet.decrypt(content.encode())).decode()
    return decrypted_content