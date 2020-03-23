import feedparser as fp
import json
import csv
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime

# Set the limit for number of articles to download
LIMIT = 52

data = {}
data['newspapers'] = {}
print(data)

# Loads the JSON files with news sites
with open('NewsPapers.json') as data_file:
    companies = json.load(data_file)

count = 1

# Iterate through each news company
with open('employee_file2.csv', mode='w',encoding='utf-8') as csv_file:
    fieldnames = ['link', 'article_link','article_published','article_title','article_text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for company, value in companies.items():
        if 'rss' in value:
            d = fp.parse(value['rss'])
            print("Downloading articles from ", company)
            for entry in d.entries:
                if hasattr(entry, 'published'):
                    if count > LIMIT:
                        break
                    article = {}
                    article['link'] = entry.link
                    date = entry.published_parsed
                    article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                    try:
                        content = Article(entry.link)
                        content.download()
                        content.parse()
                    except Exception as e:
                        # If the download for some reason fails (ex. 404) the script will continue downloading
                        # the next article.
                        print(e)
                        print("continuing...")
                        continue
                    article['title'] = content.title
                    article['text'] = content.text
                    writer.writerow({ 'link': value['link'],'article_link':article['link'],'article_published':article['published'],'article_title':article['title'],'article_text':article['text']})
                    print(count, "articles downloaded from", company, ", url: ", entry.link)
                    count = count + 1
        else:
            print("Building site for ", company)
            paper = newspaper.build(value['link'], memoize_articles=False)
            noneTypeCount = 0
            for content in paper.articles:
                if count > LIMIT:
                    break
                try:
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continuing...")
                    continue
                # Again, for consistency, if there is no found publish date the article will be skipped.
                # After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.
                if content.publish_date is None:
                    print(count, " Article has date of type None...")
                    noneTypeCount = noneTypeCount + 1
                    if noneTypeCount > 10:
                        print("Too many noneType dates, aborting...")
                        noneTypeCount = 0
                        break
                    count = count + 1
                    continue
                article = {}
                article['title'] = content.title
                article['text'] = content.text
                article['link'] = content.url
                article['published'] = content.publish_date.isoformat()
                writer.writerow({ 'link': value['link'], 'article_link': article['link'],
                                 'article_published': article['published'], 'article_title': article['title'],
                                 'article_text': article['text']})
                print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
                count = count + 1
                noneTypeCount = 0
        count = 1








