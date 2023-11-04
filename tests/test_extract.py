import pytest
from lxml import etree
from bs4 import BeautifulSoup
from lxml.html import HtmlElement
from src.bluemoss import Node, Ex, extract
from .constants import WITH_LINKS_HTML as HTML


def test_text_extraction():
    node = Node('p', extract=Ex.TEXT)
    assert extract(node, HTML) == 'Lorem 1'

    node = Node('div', extract=Ex.TEXT)
    assert extract(node, HTML) == 'Ipsum 2'


def test_full_text_extraction():
    node = Node('div', extract=Ex.FULL_TEXT)
    assert extract(node, HTML) == 'Ipsum 2\nLorem 2\nLink 2'


def test_bs4_tag_extraction():
    node = Node('div', extract=Ex.BS4_TAG)
    tag: BeautifulSoup = extract(node, HTML)
    assert isinstance(tag, BeautifulSoup)

    node = Node('div')
    assert extract(node, str(tag.prettify())) == 'Ipsum 2\nLorem 2\nLink 2'


def test_etree_extraction():
    # 1) extract the found tag as an etree._Element instance
    node = Node('div', extract=Ex.LXML_HTML_ELEMENT)
    elem: HtmlElement = extract(node, HTML)
    assert isinstance(elem, HtmlElement)

    # 2) transform the etree._Element into a html string and test the full-text-extraction on it
    html: str = etree.tostring(elem, method='html')  # type: ignore
    assert extract(Node('div'), html) == 'Ipsum 2\nLorem 2\nLink 2'


def test_tag_as_string_extraction():
    node = Node('div', extract=Ex.TAG_AS_STRING)
    html: str = extract(node, HTML)
    assert isinstance(html, str)
    node = Node('div')
    assert extract(node, html) == 'Ipsum 2\nLorem 2\nLink 2'


def test_href_extraction():
    node = Node('a', filter=2, extract=Ex.HREF)
    assert extract(node, HTML) == 'https://www.nvidia.com/link3?p=3&q=3'


def test_href_extraction_with_xpath():
    for node in [
        Node('a/@href', filter=2),
        Node('a/@href', filter=2, extract=Ex.HREF_BASE_DOMAIN),
        Node('a/@href', filter=2, extract='some_random_tag_attribute'),
    ]:
        assert extract(node, HTML) == 'https://www.nvidia.com/link3?p=3&q=3'


def test_href_query_extraction():
    node = Node('a', extract=Ex.HREF_QUERY)
    assert extract(node, HTML) == 'p=1&q=1'


def test_href_domain_extraction():
    node = Node('a', filter=3, extract=Ex.HREF_DOMAIN)
    assert extract(node, HTML) == 'chat.openai.com'


def test_href_base_domain_extraction():
    node = Node('a', filter=3, extract=Ex.HREF_BASE_DOMAIN)
    assert extract(node, HTML) == 'openai.com'


def test_href_endpoint_extraction():
    node = Node('a', filter=3, extract=Ex.HREF_ENDPOINT)
    assert extract(node, HTML) == '/page4/link4'


def test_href_endpoint_with_query_extraction():
    node = Node('a', filter=3, extract=Ex.HREF_ENDPOINT_WITH_QUERY)
    assert extract(node, HTML) == '/page4/link4?p=4&q=4&p=5'


def test_href_query_params_extraction():
    node = Node('a', filter=3, extract=Ex.HREF_QUERY_PARAMS)
    assert extract(node, HTML) == {'p': ['4', '5'], 'q': ['4']}


def test_extract_with_string_value():
    node = Node('a', filter=2, extract='href')
    assert extract(node, HTML) == 'https://www.nvidia.com/link3?p=3&q=3'


def test_extract_with_invalid_extract_value():
    node = Node('a', extract=None)  # type: ignore
    with pytest.raises(NotImplementedError):
        extract(node, HTML)
