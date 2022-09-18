import requests

paste_url = "http://127.0.0.1:5000/api/AHbVwS6J"

# data = {
#     'author': "NoobScience", 
#     'lang': "python",
#     'title': "Hello World",
#     'paste_content': "print('Hello World')"
# }

page = requests.get(paste_url)

print(page.content)