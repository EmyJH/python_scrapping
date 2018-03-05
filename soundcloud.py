import requests as rq
import json

# import builtwith as bw
# import urllib3 as url3
# import bs4

# on peut stipuler pip2 ou pip3 pour l'installation de package
# requete get followers xhr : javascript type json

r = rq.get(
    "https://api-v2.soundcloud.com/users/16509370/followers?offset=1518446202684&limit=12&client_id=gaM337KUCDvv9mYaL4ZCKFmDmoIAhiYQ&app_version=1518449338&app_locale=fr")

print(r.status_code)  # 200 = code http pour  dire ok , 500 erreur serveur interne, 403 : pb permission, 404
print(r.text)

if "blocked" in r.text:
    print("we've been blocked")  # pas de problème

# problème url de la requète donne à partir du n%12 followers , enlever offset pour commencer du début et changer limit pour obtenir plsu de 12 followers par requète http
# ainsi il y aura moins de tour de boucle, en testant limit 195000 on observe qu'on obtient que 200 followers

r = rq.get(
    "https://api-v2.soundcloud.com/users/16509370/followers?limit=200&client_id=gaM337KUCDvv9mYaL4ZCKFmDmoIAhiYQ&app_version=1518449338&app_locale=fr")
print(r.status_code)  # 200 = code http pour  dire ok , 500 erreur serveur interne, 403 : pb permission, 404
print(r.text)

if "blocked" in r.text: print("we've been blocked")

urlbase = "https://api-v2.soundcloud.com/users/16509370/followers?"
url_parametre = "limit=200&client_id=gaM337KUCDvv9mYaL4ZCKFmDmoIAhiYQ&app_version=1518449338&app_locale=fr"
r = rq.get(urlbase + url_parametre)
rjson = json.loads(r.text)
print(rjson)  # transforme le text en dico

followers = {}  # dico vide


def parse_json(json_data):
    for i in rjson['collection']:
        username = i['username']
        link_url = i['permalink_url']
        followers[username] = link_url
    return followers


next_href = rjson['next_href'].split("&")[0]
next_href2 = next_href + url_parametre
test = rjson['next_href']

c = 0

while test is not None :
    parse_json(rjson)
    test = rjson['next_href']
    c += 200
    print(c)
    if test is not None :
        next_href = rjson['next_href'].split("&")[0]
        next_href2 = next_href +"&"+ url_parametre
        r2 = rq.get(next_href2)
        rjson = json.loads(r2.text)
    else: next_href2 = ""


print(followers.__len__())

#with open('followers.json', 'w') as fp:
 #   json.dump(followers, fp)


