# from doctest import debug
from flask import Flask , render_template

# Scrapper
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Response
response = requests.get('https://news.ycombinator.com/news')
response2 = requests.get('https://news.ycombinator.com/news?p=2')

# Get the HTML page as Text
soup = BeautifulSoup(response.text, 'html.parser')
soup2 = BeautifulSoup(response2.text, 'html.parser')

# Get LINKS and SUBTEXT from Page=1
links = soup.select('.titlelink')
subtext = soup.select('.subtext')

# Get LINKS and SUBTEXT from Page=2
links2 = soup2.select('.titlelink')
subtext2 = soup2.select('.subtext')

# Combine LINKS and SUBTEXT Page=1 & Page=2
# Mega Link
mega_links = links+links2
mega_subtext = subtext+subtext2

# ---------------------- Scrapping Logic ---------------------- #
# Sorting By Votes


def sort_by_votes(news_list):
    return sorted(news_list, key=lambda k: k['votes'], reverse=True)


def custom_hackerNews(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        # print(idx)
        # print(item)
        title = links[idx].getText()  # Getting text from all the links.
        # None => Default parameter  # Getting href of all the links.
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            convert_points = int(vote[0].getText().replace(' points', ''))
            #                   Grab vote[0] => from class='score'
            if convert_points > 99:
                hn.append({"title": title, "link": href,
                          'votes': convert_points})
    return sort_by_votes(hn)
# ---------------------- Scrapping Logic End ---------------------- #

@app.route("/")
def hn_table():
    # li = [{'key':1,'name':"avin"}]
    li = custom_hackerNews(mega_links, mega_subtext)
    return render_template('index.html',li = li)


if __name__ == '__main__':
    app.run(debug=True)