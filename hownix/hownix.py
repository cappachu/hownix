#!/usr/bin/env python

import argparse
import requests
import pkgutil
from requests.exceptions import ConnectionError
from urllib import quote 
from pyquery import PyQuery
from clint.textui import puts, indent, colored


def request_page(url):
    """Returns a http response object corresponding to url"""
    # set User-Agent in header to receive appropriate response
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0'
    return requests.get(url, headers={'User-Agent': user_agent}).text


def retrieve_so_page_links(query):
    """Search within stackoverflow (SO) using google and retrieve links"""
    # augment query terms
    query += " linux command line"
    search_url = 'http://www.google.com/search?q=site:stackoverflow.com%20{0}'
    url = search_url.format(quote(query))
    result = request_page(url)
    html = PyQuery(result)
    return [a.attrib['href'] for a in html('.l')] or \
           [a.attrib['href'] for a in html('.r')('a')]


def load_commands():
    """Load unix/linux commands names from text file"""
    command_data = pkgutil.get_data('hownix', 'nix_commands.txt')
    return [l.strip() for l in command_data.split('\n')]
           

def line_2_cmd(line):
    """Return first word from text of line"""
    return line.text.split()[0]


def line_2_text(line):
    """Return text from line after cleansing"""
    return line.text.strip('$>').strip().split('\n')[0]


def candidate_command_line(line):
    """Return true for lines with non-blank text with more than a single word in which the first word is a unix/linux command"""
    commands = load_commands()
    return line.text is not None and \
           not line.text.isspace() and \
           len(line.text.strip().split()) > 1 and \
           line_2_cmd(line) in commands


def get_command_line(args, links):
    """Parse through StackOverflow page and identify command line corresponding to most frequently referred to command"""
    if not links:
        return False
    result_cmd_line = None
    # traverse through first 3 SO links 
    for link in links[:3]:
        page = request_page(link + '?answertab=votes')
        html = PyQuery(page)
        html_answers = html('.answercell').find('*')

        cmd_frequency = {}
        cmd_lines = {}
        lines = [(line_2_cmd(line), line_2_text(line)) for line in html_answers if candidate_command_line(line)]
        for (cmd,text) in lines:
            cmd_frequency[cmd] = cmd_frequency.get(cmd, 0) + 1
            cmd_lines.setdefault(cmd, []).append(text) 
        max_cmd = max(cmd_lines, key=cmd_frequency.get) if cmd_lines else None
        if max_cmd is not None:
            result_cmd_line = cmd_lines[max_cmd][0] # first line corresponding to command
    return result_cmd_line


def get_explanation_lines(command_line):
    """Returns list of text lines explaining command line"""
    if command_line is None:
        return None
    explain_url = 'http://www.explainshell.com/explain?cmd={0}'
    url = explain_url.format(quote(command_line))
    result = request_page(url)
    html = PyQuery(result)
    return [PyQuery(hb).text() for hb in html('.help-box')]


def print_result(command_line, explanation_lines):
    """Prints sample command line preceded by explanation"""
    if command_line and len(explanation_lines) > 1:
        title, body = explanation_lines[0], explanation_lines[1:]
        with indent(4, quote=colored.yellow('|')):
            puts()
            puts(colored.yellow(title.upper()))
            with indent(4):
                for line in body:
                    puts(line.encode('ascii', 'ignore'))
            puts()
            with indent(2, quote=colored.green('>')):
                puts(colored.green(command_line.encode('ascii', 'ignore')))
            puts()
    else:
        with indent(4, quote=colored.magenta('|')):
            puts()
            puts(colored.magenta("couldn't find an answer, try a different query"))
            puts()
        

def hownix(args):
    """Find StackOverflow pages related to query via Google. Extract command lines and explanation"""
    try:
        query = ' '.join(args['query']).replace('?', '')
        links = retrieve_so_page_links(query)     
        command_line = get_command_line(args, links)
        explanation_lines = get_explanation_lines(command_line)
        print_result(command_line, explanation_lines)
    except ConnectionError:
        puts(colored.red('Unable to connect to service'))


def main():
    parser = argparse.ArgumentParser(description='Find and Understand *NIX Commands')
    parser.add_argument('query', nargs='*', help='query')
    args = vars(parser.parse_args())
    if not args['query']:
        parser.print_help()
        return
    hownix(args)


if __name__ == '__main__':
    main()
