
import requests

u = requests.get('http://localhost:8080/hello?name=Pascal')
print(u.content.decode('utf-8'))

u = requests.get('http://localhost:8080/localtime')
print(u.content.decode('utf-8'))
