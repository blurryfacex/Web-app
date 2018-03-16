import requests,openpyxl

rep=requests.get('http://www.getuikit.net/docs/layouts_blog.html').text
rep=str(rep).encode('utf-8')
with open('file.html','wb+') as J:
    J.write(rep)
    J.close()