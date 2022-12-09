# TNPG: It's Friday!, Roster: Erica Li, Verit Li, Daniel He, Samson Wu
# SoftDev
# P01

import requests

#get all the keys
with open('keys/key_HuggingFace.txt', 'r') as f:
    KEY_HuggingFace = f.read()

with open('keys/key_LoveCalculator.txt', 'r') as f:
    KEY_LoveCalculator = f.read()

with open('keys/key_MyAnimeList.txt', 'r') as f:
    KEY_MyAnimeList = f.read()

#print(KEY_HuggingFace)

#uses AnimeChan API to get a random quote based on given anime character
def get_random_quote(character):
    url = 'https://animechan.vercel.app/api/random/character?name=' + character
    res = requests.get(url) 
    json = res.json() 
    quote = json['quote']
    return quote
#print('get_random_quote test:\n' + get_random_quote('tanjiro'))

#uses Kitsu API to get anime character image
# def get_image(character):
    