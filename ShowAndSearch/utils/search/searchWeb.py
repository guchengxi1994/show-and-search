'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-17 11:11:36
LastEditors: xiaoshuyui
LastEditTime: 2020-09-17 14:29:53


USELESS

'''

import requests
import os
from pyquery import PyQuery as pq
from urllib.request import getproxies
from urllib.parse import quote as url_quote, urlparse, parse_qs
from ShowAndSearch.utils.logger import logger
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
import re
from requests.exceptions import SSLError
import json

URL =  'stackoverflow.com'

NO_ANSWER_MSG = '< no answer given >'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'), )

web = {
    'bing': 'http://www.bing.com/search?q={0}%20{1}',
}

BLOCKED_QUESTION_FRAGMENTS = (
    'webcache.googleusercontent.com',
)

searchSession = requests.session()

BLOCK_INDICATORS = (
    'form id="captcha-form"',
    'This page appears when Google automatically detects requests coming from your computer '
    'network which appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service'
)

ANSWER_HEADER = '{2}  Answer from {0} {2}\n{1}'
STAR_HEADER = '\u2605'

def random_int(width):
    bres = os.urandom(width)
    ires = int.from_bytes(bres, 'little')
    return ires


def _extract_links(html, search_engine='bing'):
    html.remove_namespaces()
    with open('D:\\testALg\\ShowAndSearch\\show-and-search\\testscripts\\1.html','w',encoding='utf-8') as f:
        f.write(str(html))
    return [a.attrib['href'] for a in html('.b_algo')('h2')('a')]




def random_choice(seq):
    return seq[random_int(1) % len(seq)]

def get_link_at_pos(links, position):
    if not links:
        return False

    if len(links) >= position:
        link = links[position - 1]
    else:
        link = links[-1]
    return link

def get_proxies():
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = 'http://%s' % value
            else:
                filtered_proxies[key] = value
    return filtered_proxies

def _get_result(url):
    try:
        return searchSession.get(url, headers={'User-Agent': random_choice(USER_AGENTS)},
                                  proxies=get_proxies(),
                                  verify=True).text
    except requests.exceptions.SSLError as error:
        logger.error('Encountered an SSL Error. Try using HTTP instead of HTTPS ".\n')
        raise error

def _add_links_to_text(element):
    hyperlinks = element.find('a')

    for hyperlink in hyperlinks:
        pquery_object = pq(hyperlink)
        href = hyperlink.attrib['href']
        copy = pquery_object.text()
        if (copy == href):
            replacement = copy
        else:
            replacement = "[{0}]({1})".format(copy, href)
        pquery_object.replace_with(replacement)

def get_text(element):
    ''' return inner text in pyquery element '''
    _add_links_to_text(element)
    try:
        return element.text(squash_space=False)
    except TypeError:
        return element.text()

def _format_output(code, args):
    if not args['color']:
        return code
    lexer = None

    # try to find a lexer using the StackOverflow tags
    # or the query arguments
    for keyword in args['query'].split() + args['tags']:
        try:
            lexer = get_lexer_by_name(keyword)
            break
        except Exception:
            pass

    # no lexer found above, use the guesser
    if not lexer:
        try:
            lexer = guess_lexer(code)
        except Exception:
            return code

    return highlight(code,
                     lexer,
                     TerminalFormatter(bg='dark'))

def _get_answer(args, links):
    link = get_link_at_pos(links, args['pos'])
    if not link:
        return False

    # cache_key = link
    # page = cache.get(link)
    # if not page:
    page = _get_result(link + '?answertab=votes')
    #     cache.set(cache_key, page)

    html = pq(page)

    first_answer = html('.answer').eq(0)

    instructions = first_answer.find('pre') or first_answer.find('code')
    args['tags'] = [t.text for t in html('.post-tag')]

    # make decision on answer body class.
    if first_answer.find(".js-post-body"):
        answer_body_cls = ".js-post-body"
    else:
        # rollback to post-text class
        answer_body_cls = ".post-text"

    if not instructions and not args['all']:
        text = get_text(first_answer.find(answer_body_cls).eq(0))
    elif args['all']:
        texts = []
        for html_tag in first_answer.items('{} > *'.format(answer_body_cls)):
            current_text = get_text(html_tag)
            if current_text:
                if html_tag[0].tag in ['pre', 'code']:
                    texts.append(_format_output(current_text, args))
                else:
                    texts.append(current_text)
        text = '\n'.join(texts)
    else:
        text = _format_output(get_text(instructions.eq(0)), args)
    if text is None:
        text = NO_ANSWER_MSG
    text = text.strip()
    return text

def _get_search_url(search_engine='bing'):
    return web.get(search_engine, web['bing'])

def _is_blocked(page):
    for indicator in BLOCK_INDICATORS:
        if page.find(indicator) != -1:
            return True

    return False

def _get_links(query):
    search_engine = 'bing'
    search_url = _get_search_url(search_engine)
    question_url = (search_url.format(URL, url_quote(query))).replace('site:','')
    # print(question_url)
    question_url = 'https://cn.bing.com/search?q=stackoverflow.com\%20\%20print\%20\stack%20trace%20python&toHttps=1&redig=4C72A2C577E941C7A802A1B46268FAAD'
    result = _get_result(question_url)

    # print(result)

    if _is_blocked(result):
        logger.error('Unable to find an answer because the search engine temporarily blocked the request. '
                   'Please wait a few minutes or select a different search engine.')
        raise RuntimeError("Temporary block by search engine")

    html = pq(result)
    return _extract_links(html, search_engine)

def _get_questions(links):
    return [link for link in links if _is_question(link)]


def _is_question(link):
    for fragment in BLOCKED_QUESTION_FRAGMENTS:
        if fragment in link:
            return False
    return re.search(r'questions/\d+/', link)


def _get_links_with_cache(query):
    links = _get_links(query)
    # print(links)
    question_links = _get_questions(links)
    return question_links


def _get_answers(args):
    """
    @args: command-line arguments
    returns: array of answers and their respective metadata
             False if unable to get answers
    """

    question_links = _get_links_with_cache(args['query'])
    if not question_links:
        return False

    # print(question_links)

    answers = []
    initial_position = args['pos']
    multiple_answers = (args['num_answers'] > 1 or args['all'])

    for answer_number in range(args['num_answers']):
        current_position = answer_number + initial_position
        args['pos'] = current_position
        link = get_link_at_pos(question_links, current_position)
        answer = _get_answer(args, question_links)
        if not answer:
            continue
        if not args['link'] and not args['json_output'] and multiple_answers:
            answer = ANSWER_HEADER.format(link, answer, STAR_HEADER)
        answer += '\n'
        answers.append({
            'answer': answer,
            'link': link,
            'position': current_position
        })

    return answers


def build_splitter(splitter_character='=', splitter_length=80):
    return '\n' + splitter_character * splitter_length + '\n\n'


def _format_answers(res, args):
    if "error" in res:
        return res["error"]

    if args["json_output"]:
        return json.dumps(res)

    formatted_answers = []

    for answer in res:
        next_ans = answer["answer"]
        if args["link"]:  # if we only want links
            next_ans = answer["link"]
        formatted_answers.append(next_ans)

    return build_splitter().join(formatted_answers)



def _parse_cmd(args, res):
    answer = _format_answers(res, args)
    # cmd_key = _get_stash_key(args)
    # title = ''.join(args['query'])
    # if args[STASH_SAVE]:
    #     _stash_save(cmd_key, title, answer)
    #     return ''

    # if args[STASH_REMOVE]:
    #     _stash_remove(cmd_key, title)
    #     return ''
    return answer

def script(question:str):
    args = dict()
    args['query'] = question
    try:
        res = _get_answers(args)
        if not res:
            res = {'error': 'Sorry, couldn\'t find any help with that topic\n'}
        # cache.set(cache_key, res)
    except (ConnectionError, SSLError):
        res = {'error': 'Unable to reach {search_engine}. Do you need to use a proxy?\n'.format(
            search_engine=args['search_engine'])}
    
    return _parse_cmd(args, res)