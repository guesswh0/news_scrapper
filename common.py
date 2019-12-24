import io

import bs4
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests


def get_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        proxies=None
):
    """Get session with retries and proxies"""
    session = requests.Session()
    if proxies:
        session.proxies = proxies
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_text_from_tag(tag: bs4.element.Tag):
    """Unwraps tags and nested tags contents"""
    if tag.string:
        return tag.string
    text = ''
    if len(tag) > 1:
        for t in tag:
            text += get_text_from_tag(t)
    return text


def get_news_full_text(url, session=None):
    """Extracts and concatenates all article text from url"""
    session = session or get_session()
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # todo нашел только два вида новостей
    result = soup.find('div', 'fullnews white_block')
    if not result:
        result = soup.find('div', 'WordSection1')

    buff = io.StringIO()
    try:
        for tag in result.findAll('p')[:-1]:
            text = get_text_from_tag(tag)
            if text:
                buff.write(text.replace('\r', '').replace('\n', ' '))
                buff.write('\n')
    except AttributeError:
        pass
    return buff.getvalue()
