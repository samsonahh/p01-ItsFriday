# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

import requests

#get all the keys
with open('app/keys/key_HuggingFace.txt', 'r') as f:
    KEY_HuggingFace = f.read()

with open('app/keys/key_LoveCalculator.txt', 'r') as f:
    KEY_LoveCalculator = f.read()

with open('app/keys/key_MyAnimeList.txt', 'r') as f:
    KEY_MyAnimeList = f.read()

#print(KEY_HuggingFace)

#uses AnimeChan API to get a random quote based on given anime character
def get_random_quote(character):
    url = 'https://animechan.vercel.app/api/random/character?name=' + character
    res = requests.get(url) 
    json = res.json() 
    quote = json['quote']
    #character = json['character']
    return quote
#print('get_random_quote test:\n' + get_random_quote('tanjiro'))
#uses Kitsu API to get anime character image
#def get_image(character):
    # url =  "https://kitsu.io/api/edge/characters?"
    # res = requests.get(url, params={"filter[name]": character})
    # return res.json()

#uses AnimeChan API to get a random character and their quotes and their information from Kitsu API
def get_random_profile():
    #First get a random character with eligible quotes
    AnimeChan_url = 'https://animechan.vercel.app/api/random'
    res = requests.get(AnimeChan_url) 
    json = res.json() 
    character = json['character'] #Use accurate name returned by animechan to search in Kitsu API
    url =  "https://kitsu.io/api/edge/characters?"
    res = requests.get(url, params={"filter[name]": character})
    #Only looks at the first character returned
    json = res.json()
    en_name = json["data"][0]["attributes"]["names"]["en"]
    jp_name = json["data"][0]["attributes"]["names"]["ja_jp"]
    description = json["data"][0]["attributes"]["description"]
    image = json["data"][0]["attributes"]["image"]["original"]
    #find ten quotes from animechan 
    AnimeChan_url_ten = "https://animechan.vercel.app/api/quotes/character?name=" + character
    res = requests.get(AnimeChan_url_ten) 
    json = res.json()
    quotes = []
    for data in json:
        quotes.append(data['quote'])
    return {"name": en_name, "description": description, "image": image, "quotes": quotes}

def query_character(input):
    print("Keep in mind the API limit!")
    url =  "https://kitsu.io/api/edge/characters?"
    res = requests.get(url, params={"filter[name]": input})
    json = res.json()
    output = []
    for data in json["data"]: 
        en_name = data["attributes"]["names"]["en"]
        # if data["attributes"]["names"]["ja_jp"] is None: 
        #     jp_name = "None"
        # else: 
        #     jp_name = data["attributes"]["names"]["ja_jp"]
        description = data["attributes"]["description"]
        print (description)
        if data["attributes"]["image"] is None:
            image = "https://media.kitsu.io/characters/images/8266/original.jpg"
        else :
            image = data["attributes"]["image"]["original"]
        output.append({"name": en_name, "description": description, "image": image})
    return output 

def helper_page_format(page): # page is given as a string, convert into int. Page used as the value of offset attribute in Kitsu API calls 
    page = int(page)
    if page < 0:
        page = 0
    return page * 12 # the page "offset" needs to be 12 because each page displays 12 items 

def pagination(input, page):
    print("Keep in mind the API limit!")
    page = helper_page_format(page)
    # print (page)
    # print(123//10 + 1)
    url =  f"https://kitsu.io/api/edge/characters?page[limit]=12&page[offset]={page}"
    res = requests.get(url, params={"filter[name]": input})
    json = res.json()
    output = []
    max = json["meta"]['count']
    for data in json["data"]: 
        id = data["id"]
        en_name = data["attributes"]["names"]["en"]
        # Sometimes jp name is null...
        # if data["attributes"]["names"]["ja_jp"] is None: 
        #     jp_name = "None"
        # else: 
        #     jp_name = data["attributes"]["names"]["ja_jp"]
        description = data["attributes"]["description"]
        if data["attributes"]["image"] is None:
            image = "https://media.kitsu.io/characters/images/8266/original.jpg"
        else :
            image = data["attributes"]["image"]["original"]
        output.append({"name": en_name, "description": description, "image": image, "id": id})
    return (output, max) # use max to figure out pagination 

def pagination_with_media(input, page, media):
    print("Keep in mind the API limit!")
    page = helper_page_format(page)
    output = []
    if media == 'Character':
        return pagination(input, page)
    elif media == 'Show':
        url = f"https://kitsu.io/api/edge/anime?page[limit]=12&page[offset]={page}"
        res = requests.get(url, params={"filter[text]": input})
        json = res.json()
        max = json["meta"]['count']
        for data in json["data"]:
            id = data['id']
            en_name = data["attributes"]["canonicalTitle"]
            synopsis = data["attributes"]["synopsis"]
            average_rating = data["attributes"]["averageRating"]
            start_date = data["attributes"]["startDate"]
            if data["attributes"]["posterImage"] is None:
                image = "https://media.kitsu.io/characters/images/8266/original.jpg"
            else :
                image = data["attributes"]["posterImage"]["original"]
            if data["attributes"]["coverImage"] is None:
                cover_image = "https://media.kitsu.io/characters/images/8266/original.jpg"
            else :
                cover_image = data["attributes"]["coverImage"]["original"]
           # characters = data["relationships"]["characters"]["links"]["related"]
            output.append({"title" : en_name, "synopsis": synopsis, "rating": average_rating, "date": start_date, "image": image, "cover": cover_image, 'id': id})
    else: 
        max = 0
        print ("Dangerous!")
    return (output, max) # use max to figure out pagination 

def pagination_id(id, page):
    page = helper_page_format(page)
    url = f"https://kitsu.io/api/edge/anime/{id}/anime-characters?page[limit]=12&page[offset]={page}"
    res = requests.get(url)
    json = res.json()
    max = json["meta"]['count']
    output = []
    for data in json["data"]:
        character_url = data["relationships"]["character"]["links"]["related"]
        res = requests.get(character_url)
        json = res.json()
        data = json['data']
        id = data["id"]
        en_name = data["attributes"]["names"]["en"]
        # Sometimes jp name is null...
        # if data["attributes"]["names"]["ja_jp"] is None: 
        #     jp_name = "None"
        # else: 
        #     jp_name = data["attributes"]["names"]["ja_jp"]
        description = data["attributes"]["description"]
        print (description)
        if data["attributes"]["image"] is None:
            image = "https://media.kitsu.io/characters/images/8266/original.jpg"
        else :
            image = data["attributes"]["image"]["original"]
        output.append({"name": en_name, "description": description, "image": image, "id": id})
    return (output, max)
