import requests
import random

def download_list(url):
    r = requests.get(url)
    return [x.strip() for x in r.text.split('\n') if x.strip() != '']

nouns = download_list('http://www.desiquintans.com/downloads/nounlist/nounlist.txt')
verbs = download_list('https://raw.githubusercontent.com/aaronbassett/Pass-phrase/master/verbs.txt')

formats = [
    lambda v, n: f'{v()} {n()}',
    lambda _, n: f'{n()} of {n()}'
]

def make_spell():
    return random.choice(formats)(lambda: random.choice(verbs), lambda: random.choice(nouns))

if __name__ == "__main__":
    for _ in range(20):
        print(make_spell())
