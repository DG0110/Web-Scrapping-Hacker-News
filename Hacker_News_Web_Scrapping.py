import requests
from bs4 import BeautifulSoup
import pandas as pd
def create_custom_fn(links, subtext, author, user):
    hn = []
    for idx, item in enumerate(links):
        titles = links[idx].getText()
        link = links[idx].find('a').get('href', None)
        if idx < len(author):
            current_author = author[idx].getText()
        if idx < len(user):
            current_user = user[idx].getText()
        vote = subtext[idx].select('.score')
        if len(vote):
            vote = int(vote[0].getText().replace(' points', ''))
            if vote > 1:
                hn.append(dict
                          (title=titles,
                           links=link,
                           votes=vote,
                           author=current_author,
                           user=current_user))
    return sort_fun(hn)

#sort_fun will sort the result on the basis of votes

def sort_fun(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Define the URL and the number of pages to scrape
hacker_news_url = 'https://news.ycombinator.com/news'
num_pages_to_scrape = 6  #the number of pages we want to scrape

def scrape_hacker_news(url, pages):
    all_data = []

    for page in range(1, pages + 1):
        page_url = f'{url}?p={page}'
        try:
            res = requests.get(page_url)
            res.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(res.text, 'lxml')

        subtext = soup.select('.subtext')
        links = soup.select('.titleline')
        author = soup.select('.sitestr')
        user = soup.select('.hnuser')

        data = create_custom_fn(links, subtext, author, user)
        all_data.extend(data)

    return all_data




# Scrape data from multiple pages
all_hacker_news_data = scrape_hacker_news(hacker_news_url, num_pages_to_scrape)

# Create DataFrame and save to Excel
df = pd.DataFrame(all_hacker_news_data)
print(df)
df.to_excel('hacker_multi_pages.xlsx', index=False)
