from bs4 import BeautifulSoup
import requests

def retrieve_nyt():
    r = requests.get("https://www.nytimes.com/puzzles/sudoku/easy")
    soup = BeautifulSoup(r.text,'html.parser')
    s = soup.find_all("script")[0].string
    eraw = s[357:518].split(',')
    easy = [[int(eraw[9*i+j]) for j in range(9)] for i in range(9)]
    easy_long = [int(i) for i in eraw]
    mraw = s[1728:1889].split(',')
    medium = [[int(mraw[9*i+j]) for j in range(9)] for i in range(9)]
    medium_long = [int(i) for i in mraw]
    hraw = s[1035:1196].split(',')
    hard = [[int(hraw[9*i+j]) for j in range(9)] for i in range(9)]
    hard_long = [int(i) for i in hraw]
    return [easy,medium,hard,easy_long,medium_long,hard_long]


def convert(s):
    s = s.split(',')
    return [int(i) for i in s]


if __name__ == '__main__':
    [e,m,h,el,ml,hl] = retrieve_nyt()
    print(el)
    print(ml)
    print(hl)
    [print(i) for i in e]
    print()
    [print(i) for i in m]
    print()
    [print(i) for i in h]
    print()
