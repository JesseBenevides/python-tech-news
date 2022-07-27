import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        res = requests.get(url, timeout=3)
        res.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    return res.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    links = selector.css("a.cs-overlay-link::attr(href)").getall()
    return links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    link = selector.css("a.next::attr(href)").get()
    return link


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)

    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a::text").get()
    comments_count = selector.css(
        "div.post-comments h5.title-block::text"
    ).get()
    summary = "".join(
        selector.css("div.entry-content > p:nth-of-type(1) ::text").getall()
    ).strip()
    tags = selector.css("section.post-tags a::text").getall()
    category = selector.css("span.label::text").get()

    if comments_count is None:
        comments_count = 0
    else:
        comments_count = int(
            comments_count.replace("\n", "").replace("\t", "").split(" ")[0]
        )

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": summary,
        "tags": tags,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    html_content = fetch("https://blog.betrybe.com")
    novidades = scrape_novidades(html_content)
    news = list()

    while amount >= 1:
        for link in novidades[0:amount]:
            content = fetch(link)
            news.append(scrape_noticia(content))
            amount -= 1
        if amount >= 1:
            next_page_link = scrape_next_page_link(html_content)
            html_content = fetch(next_page_link)
            novidades = scrape_novidades(html_content)

    create_news(news)
    return news
