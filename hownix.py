#!/usr/bin/env python

# suggest commonly co-used arguments
# search through shell history
# screenshots in case explain shell goes down, fork explain shell
import argparse
import requests
from requests.exceptions import ConnectionError
from urllib import quote 
from pyquery import PyQuery
from clint.textui import puts, indent, colored

def request_page(url):
    #print url
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

def get_command_line(args, link):
    if not link:
        return False
    page = request_page(link + '?answertab=votes')
    html = PyQuery(page)

    commands = [l.strip() for l in open('nix_commands.txt').readlines()]
    cmd_frequency = {}
    cmd_lines = {}
    max_cmd = None
    max_freq = 0
    html_answers = html('.answercell').find('*')
    for line in html_answers:
        if line is not None and line.text is not None and not line.text.isspace() and len(line.text.strip().split()) > 1: 
            line_text = line.text.strip('$>').strip().split('\n')[0]

            cmd = line.text.strip('$>').strip().split()[0]
            if cmd in commands:
                cmd_frequency[cmd] = cmd_frequency.get(cmd, 0) + 1
                cmd_lines.setdefault(cmd, []).append(line_text)
                if cmd_frequency > max_freq:
                    max_freq = cmd_frequency
                    max_cmd = cmd
    if max_cmd is not None:
        return cmd_lines[max_cmd][0]
    
    # TODO handle case in which None is returned
    return None 


def get_explanation_lines(command_line):
    if command_line is None:
        return None
    explain_url = 'http://www.explainshell.com/explain?cmd={0}'
    url = explain_url.format(quote(command_line))
    result = request_page(url)
    html = PyQuery(result)
    return [PyQuery(hb).text() for hb in html('.help-box')]

def print_result(command_line, explanation_lines):
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
            puts(colored.magenta("sorry, I don't understand your query, try a different query"))
            puts()
        
        # TODO remove DEBUG print statements
        #print command_line
        #print explanation_lines


def hownix(args):
    try:
        query = ' '.join(args['query']).replace('?', '')
        links = retrieve_so_page_links(query)     
        if not links:
            return False
        command_line = get_command_line(args, links[0])
        explanation_lines = get_explanation_lines(command_line)
        print_result(command_line, explanation_lines)
    except ConnectionError:
        print 'Unable to connect to service'


def main():
    parser = argparse.ArgumentParser(description='find and understand *nix commands')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='query')
    args = vars(parser.parse_args())
    if not args['query']:
        parser.print_help()
        return
    hownix(args)


if __name__ == '__main__':
    main()
