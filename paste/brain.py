from paste.models import Bin
import random
import string
from datetime import datetime, date
from paste import app, db
import json
import requests
import pyjokes

def hash_engine():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    whole =  lower + upper + digits
    hash_string = random.sample(whole, 8)
    hash = "".join(hash_string)
    return hash

def time_cal():
    current_t = datetime.now()
    current_date = str(date.today())
    current_t_f = current_t.strftime("%H:%M:%S")
    timeAnddate = (f'{current_t_f} {current_date}')
    return timeAnddate

def add_to_db(title, content, author, lang):
    hash = hash_engine()
    time = time_cal()
    paste_info = Bin(title=title, hash=hash, content=content, lang=lang, author=author, time=time)
    db.session.add(paste_info)
    db.session.commit()
    paste_info = {"title": title, "hash": hash, "content": content, "lang": lang, "author": author}
    return paste_info

def get_db(hash):
    content = Bin.query.filter_by(hash=hash).first()
    if content == None:
        return "No Such Paste"
    else:
        return content

def debug_engine():
    debug_content = Bin.query.all()
    return debug_content

def undo():
    db.session.rollback()

def ran_quote():
    quotes_page = json.loads(requests.get("https://api.quotable.io/random").content)
    quote_list = [quotes_page["content"], quotes_page["author"]]
    return quote_list

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

def qr_code_engine(url):
    import pyqrcode
    qr_code = pyqrcode.create(url)
    qr_code.svg('paste/static/assets/images/qr_code.svg', background="white", scale=8)