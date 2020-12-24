from bs4 import BeautifulSoup
import requests

def retrieve():
    r = requests.get("https://www.nytimes.com/puzzles/sudoku/easy")
    soup = BeautifulSoup(r.text,'html.parser')
    s = soup.find_all("script")[0].string
    eraw = s[357:518].split(',')
    easy = [[int(eraw[9*i+j]) for j in range(9)] for i in range(9)]
    mraw = s[1728:1889].split(',')
    medium = [[int(mraw[9*i+j]) for j in range(9)] for i in range(9)]
    hraw = s[1035:1196].split(',')
    hard = [[int(hraw[9*i+j]) for j in range(9)] for i in range(9)]
    return [easy,medium,hard,s[357:518],s[1728:1889],s[1035:1196]]


if __name__ == '__main__':
    [e,m,h,el,ml,hl] = retrieve()
    [print(i) for i in e]
    print()
    [print(i) for i in m]
    print()
    [print(i) for i in h]
    print()
