import requests
from bs4 import BeautifulSoup
import pprint  # pretty print

response = requests.get('https://news.ycombinator.com/news')
response2 = requests.get('https://news.ycombinator.com/news?p=2')

# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')
soup2 = BeautifulSoup(response2.text, 'html.parser')


# get Links from class='titlelink'
links = soup.select('.titlelink')
links2 = soup2.select('.titlelink')
# print(links)

# Get Score from class='subtext' and the select class='score'
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

# Mega Link
mega_links = links+links2
mega_subtext = subtext+subtext2

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


pprint.pprint(custom_hackerNews(mega_links, mega_subtext))


# ------------------------------ Worked --------------------------------- #
# # Get Data For Next Page
# current_page = soup.find("a", class_="morelink").get('href')
# next_page = current_page.replace('=2','=3')
# print(next_page)
# print(current_page)
