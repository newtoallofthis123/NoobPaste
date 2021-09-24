# NoobPaste
<img src="paste/static/assets/icons/icon.png" alt="NoobPaste Image" width=400px align="right">
NoobPaste is written in python using the flask micro framework. It is very fast and is very secure. 
NoobPaste uses a database to store your data. The data is acessed using postgregsql. 
This setup should be relatively safe. Your Code is stored in a database which is queried everytime you make a request. 
<br><br>
Unless you have the exact 8 character string, accidentally stubling onto another code is quite rare. Password protection is coming soon. 
NoobPaste is deployed on heroku. Heroku servers take some time to activate but once they do, they are relatively fast. (sorry for using the word 'relatively' so much 🙂). 
NoobPaste is simply meant to act as a good alternative to pastebin and it is till in beta. So, use it with care and don't post anything sensitive on it.

<br><br>
NoobPaste has a strict no tracking policy. NoobPaste can't track you because 1. It doesn't want to 2. It can't because I don't have the necessary skills to track 😄. You can rest assured NoobPaste won't track you.
<br><br>
NoobPaste does use cookies. When you create a new paste, your author field and paste_id is stored locally in the cookies. These cookies are only used when you visit NoobPaste, to show your author and last paste. These are not cross site cookies and are not harmfull for your computer. These are pretty much harmless and have no valid information. NoobPaste has no reason to track you at all. 😌
<br><br>
NoobPaste is opensource and is it's code is hosted on github. Although the github repository is not linked to the heroku depolyment, so except regular updates in the github repository which may not be pushed to heroku. NoobPaste's github repository is <code>https://github.com/newtoallofthis123/NoobPaste</code>. Any help is appreciated. NoobPaste can also be self hosted on heroku. All you have to do this replace all the instances of NoobPaste with your heroku app name and you are done 😋. You can also run NoobPaste on replit. Heroku Template coming soon.

# API Usage

POST API

``` shell
curl -X POST -d 'author=noobscience&title=hello_world&lang=python&content=print("Hello World")' https://noobpost.herokuapp.com/api
```

GET API

``` shell
curl -X GET https://noobpost.herokuapp.com/api/AHbVwS6J
```
