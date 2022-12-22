# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

import requests
import os 
#get all the keys
def apparatus_key_HuggingFace():
    try:
        wd = os.path.dirname(os.path.realpath(__file__))
        file = open(wd + "/keys/key_HuggingFace.txt", "r")
        key = file.read()
        return key
    except: 
        return 'False'
        
def apparatus_key_LoveCalculator():
    try:
        wd = os.path.dirname(os.path.realpath(__file__))
        file = open(wd + "/keys/key_LoveCalculator.txt", "r")
        key = file.read()
        return key
    except: 
        return 'False'
    
def apparatus_key_MyAnimeList():
    try:
        wd = os.path.dirname(os.path.realpath(__file__))
        file = open(wd + "/keys/key_MyAnimeList.txt", "r")
        key = file.read()
        return key
    except: 
        return 'False'

# print(apparatus_key_HuggingFace())
# with open('app/keys/key_HuggingFace.txt', 'r') as f:
#     KEY_HuggingFace = f.read()

# with open('app/keys/key_LoveCalculator.txt', 'r') as f:
#     KEY_LoveCalculator = f.read()

# with open('app/keys/key_MyAnimeList.txt', 'r') as f:
#     KEY_MyAnimeList = f.read()

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
def get_random_profile(): # OUTDATED 
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

def query_character(input): #OUTDATED
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
    page = int(page) - 1
    if page < 0:
        page = 0
    print('AAAAAA')
    print(page * 12)
    print('AAAAAA')
    return page * 12 # the page "offset" needs to be 12 because each page displays 12 items 

def pagination(input, page):
    print("Keep in mind the API limit!")
    page = helper_page_format(page)
    print (page)
    # print(123//10 + 1)
    url =  f"https://kitsu.io/api/edge/characters?page[limit]=12&page[offset]={page}"
    res = requests.get(url, params={"filter[name]": input})
    json = res.json()
    output = []
    max = (int(json["meta"]['count']) // 12) + 1
    if max == 0:
        max = 1
    for data in json["data"]: 
        id = data["id"]
        en_name = data["attributes"]["names"]["en"]
        # Sometimes jp name is null...
        # if data["attributes"]["names"]["ja_jp"] is None: 
        #     jp_name = "None"
        # else: 
        #     jp_name = data["attributes"]["names"]["ja_jp"]
        description = data["attributes"]["description"]
        #print(description)
        if len(description) == 0 or description == '\nNo biography written.\n\n':
            continue
        if data["attributes"]["image"] is None:
            continue
        else :
            image = data["attributes"]["image"]["original"]
        output.append({"name": en_name, "description": description, "image": image, "id": id})
    return (output, max) # use max to figure out pagination 

def pagination_with_media(input, page, media):
    print("Keep in mind the API limit!")
    output = []
    if media == 'Character':
        return pagination(input, page)
    elif media == 'Show':
        page = helper_page_format(page)
        url = f"https://kitsu.io/api/edge/anime?page[limit]=12&page[offset]={page}"
        res = requests.get(url, params={"filter[text]": input})
        json = res.json()
        max = (int(json["meta"]['count']) // 12) + 1
        if max == 0:
            max = 1
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
    max = (int(json["meta"]['count']) // 12) + 1
    if max == 0:
        max = 1
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
        #print (description)
        if data["attributes"]["image"] is None:
            image = "https://media.kitsu.io/characters/images/8266/original.jpg"
        else :
            image = data["attributes"]["image"]["original"]
        output.append({"name": en_name, "description": description, "image": image, "id": id})
    return (output, max)

#Takes in two characters and returns a compatibility percentage (0.0 to 1.0) based on the LoveCalculator API
def LoveCalculator_calculate(character0, character1):
    url = "https://love-calculator.p.rapidapi.com/getPercentage"
    querystring = {"sname":character0,"fname":character1}

    headers = {
        "X-RapidAPI-Key": apparatus_key_LoveCalculator(),
        "X-RapidAPI-Host": "love-calculator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        json = response.json()
        compatibility = json["percentage"] #NOTE: this returns a string of an integer number 0-100
        compatibility = float(compatibility) / 100.0
    else: 
        compatibility = -1 #NOTE: if key is missing or does not work, -1 is returned 
    return compatibility
#LoveCalculator_calculate() tests:
# print(LoveCalculator_calculate("Bobby", "Bobaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
#print(type(LoveCalculator_calculate("John", "Alice")))

#Uses AnimeChan API to get a list of 10 quotes for an inputed anime character
def get_ten_quotes(character, boolean):
    url = 'https://animechan.vercel.app/api/quotes/character?name=' + character
    res = requests.get(url) 
    json = res.json() #returns a list of dictionaries
    #print(type(json))
    # print(json)
    if 'error' not in json:
        quote = json[0]['quote']
        if len(json) > 1:
            valid_name = json[1]['character']
        else:
            valid_name = json[0]['character']
        # print (valid_name)
        if valid_name != character and boolean:
            return []
        list = []
        for i in json: #for each one of the dictionaries in json (which each has a quote)...
            #print(i)
            list.append(i['quote'])
        #print(list) 
        list.append(valid_name)
        return list
    else:
        if boolean:
            txt = character.split()
            if len(txt) == 1:
                return []
            else:
                list = get_ten_quotes(txt[0], False)
                print(list)
                if list == []:
                    return []
                else:
                    for tx in txt:
                        if tx not in list[-1]:
                            return []
                return list
        return []
#test for get_ten_quotes
# print(get_ten_quotes('Asuka Langley Souryuu', True))
#print(['a'] == [])
#Uses HuggingFace API to get a quote analysis for an inputed string
#returns a dictionary filled with keys pertaining to the emotions:
#anger, disgust, fear, joy, neutral, sadness, and surprise
def quote_analysis(quote):
    API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    API_TOKEN = apparatus_key_HuggingFace()
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, data = {"inputs": quote}, headers = {"Authorization": f"Bearer {API_TOKEN}"})
    print(response.json())
    if 'error' in response.json():
        return {'neutral': 0.94, 'surprise':0.01, 'sadness':0.01, 'anger':0.01, 'joy':0.01, 'disgust':0.01,'fear':0.01}
    response = response.json()[0]
    emotion_dict = {}
    for i in response:
        emotion_dict[i['label']] = i['score']
    return(emotion_dict)
#print('quote_analysis(quote) function tests:')
#print(quote_analysis("hi"))
#print(quote_analysis("i am happy"))


#takes in a list of quotes and returns the a dictionary with the mean of each sentiment
#used in the quote_analysis(quote) function
def ten_quote_analysis(quotes_list):
    #set up initial averaged_emotion_dict
    averaged_emotion_dict = {'neutral': 0.0, 'surprise':0.0, 'sadness':0.0, 'anger':0.0, 'joy':0.0, 'disgust':0.0,'fear':0.0}
   
    #accumulate all emotion ratings of the 10 quotes
    for i in quotes_list: 
        emotion_dict = quote_analysis(i)
        for emotion in emotion_dict:
            #print(emotion + ": " + str(averaged_emotion_dict[emotion]))  #this is test code
            averaged_emotion_dict[emotion] += emotion_dict[emotion] 
        #print("-----")   #this is test code
        
    #divide by 10 for each emotion to get the mean
    for emotion in averaged_emotion_dict:
        averaged_emotion_dict[emotion] /= int(len(quotes_list))
        #print(emotion + ": " + str(averaged_emotion_dict[emotion]))  #this is test code
        
    return averaged_emotion_dict
#print(get_ten_quotes('Naruto Uzumaki'))            
# print(ten_quote_analysis(get_ten_quotes('Naruto Uzumaki', True)))     

'''
1. Find the mean of each sentiment given a list of quote analyses respective to a character. 
2. Isolate major sentiments from Hugging face Dataset for characters A and B
3. Compare each major sentiment from character A to the same sentiment found in character B and find similarity of the two percentages through:   
               1 - (|A-B| / max(A,B))	  (repeat for all major sentiments)
4. Repeat previous step for character B 
5. Find the mean of all the similarity percentages calculated in steps 2,3
6. Weigh the sentiment similarity and love calculator compatibility, add, then curve the result as needed 
'''
def calculate_final_compatibility(character0, character1):
    LoveCalculator_compatibility = LoveCalculator_calculate(character0, character1)
    character0_quotes = get_ten_quotes(character0, True)
    character1_quotes = get_ten_quotes(character1, True)
    if character0_quotes != []:
        character0_quotes.pop()
    if character1_quotes != []:
        character1_quotes.pop()
    #step 1:
    sentiments_character0 = ten_quote_analysis(character0) #this is a dictionary
    sentiments_character1 = ten_quote_analysis(character1)
    
    #step 2: isolate major sentiments (major sentiment defined as >40% for now)
    major_sentiment_threshold = 0.14
    major_sentiments = []
    for emotion in sentiments_character0:
        if sentiments_character0[emotion] >= major_sentiment_threshold:
            major_sentiments.append(emotion)
    for emotion in sentiments_character0:
        if sentiments_character0[emotion] >= major_sentiment_threshold and major_sentiments.count(emotion) == 0:
            major_sentiments.append(emotion)
    
    #step 3 (and 4):
    major_sentiment_similarity = {}
    for emotion in  major_sentiments:
        major_sentiment_similarity[emotion] = 1 - (abs(sentiments_character0[emotion] - sentiments_character1[emotion])/  \
                                                   max(sentiments_character0[emotion], sentiments_character1[emotion]))
    
    #step 5:
    mean_major_sentiment_similarity = 0
    for emotion in major_sentiment_similarity:
        mean_major_sentiment_similarity += major_sentiment_similarity[emotion]
    mean_major_sentiment_similarity /= len(major_sentiments)
    # print('AAAAAAAAAA')
    # print(mean_major_sentiment_similarity)
    # print(LoveCalculator_compatibility)
    # print('AAAAAAAAAA')
    #step 6:
    quote_analysis_weight = 0.86
    LoveCalculator_weight = 1.0 - quote_analysis_weight
    final_compatibility = (quote_analysis_weight * mean_major_sentiment_similarity) + \
                          (LoveCalculator_weight * LoveCalculator_compatibility)
    final_compatibility *= 100
    return {'final_compatibility': int(final_compatibility), 'character0_quotes': character0_quotes, 'character1_quotes': character1_quotes, 'sentiments_character0': sentiments_character0, 'sentiments_character1': sentiments_character1}
# print("calculate_final_compatibility(character0, character1) function test:")
# print(calculate_final_compatibility("Naruto Uzumaki", "Tanjiro Kamado"))
    
def get_char_info_by_id(id):
    url = f"https://kitsu.io/api/edge/characters/{id}"
    res = requests.get(url)
    json = res.json()
    output = []
    data = json['data']
    id = data["id"]
    en_name = data["attributes"]["names"]["en"]
        # Sometimes jp name is null...
        # if data["attributes"]["names"]["ja_jp"] is None: 
        #     jp_name = "None"
        # else: 
        #     jp_name = data["attributes"]["names"]["ja_jp"]
    description = data["attributes"]["description"]
        #print (description)
    if data["attributes"]["image"] is None:
        image = "https://media.kitsu.io/characters/images/8266/original.jpg"
    else :
        image = data["attributes"]["image"]["original"]
    output.append({"name": en_name, "description": description, "image": image, "id": id})
    return output