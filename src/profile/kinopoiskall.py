# -*- coding: UTF-8 -*-
#BY Nikolasi for indb
from __future__ import print_function
import re
from urllib2 import Request, URLError, HTTPError, urlopen as urlopen2, quote as urllib2_quote, unquote as urllib2_unquote
import urllib
from socket import gaierror, error
import httplib
import urllib
import re
import urllib2
import string
import time
import os
import socket
import sys
import traceback
import codecs
from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
std_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2',
 'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
 'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3'}


def comment_out(str):
    s = str
    try:
        s = unicode(str, 'utf8')
    except:
        pass

    print('# %s' % (s,))


def debug_out(str):
    if VERBOSE:
        comment_out(str)


def response_out(str):
    if DUMP_RESPONSE:
        s = str
        try:
            s = unicode(str, 'utf8')
        except:
            pass

        print(s)


def print_exception(str):
    for line in str.splitlines():
        comment_out(line)


def normilize_string(processingstring):
    try:
        symbols_to_remove = {'&#160;': ' ',
         '&nbsp;': ' ',
         '&#161;': '\xc2\xa1',
         '&iexcl;': '\xc2\xa1',
         '&#162;': '\xc2\xa2',
         '&cent;': '\xc2\xa2',
         '&#163;': '\xc2\xa3',
         '&pound;': '\xc2\xa3',
         '&#164;': '\xc2\xa4',
         '&curren;': '\xc2\xa4',
         '&#165;': '\xc2\xa5',
         '&yen;': '\xc2\xa5',
         '&#166;': '\xc2\xa6',
         '&brvbar;': '\xc2\xa6',
         '&brkbar;': ',',
         '&#167;': '\xc2\xa7',
         '&sect;': '\xc2\xa7',
         '&#168;': '\xc2\xa8',
         '&uml;': '\xc2\xa8',
         '&#169;': '\xc2\xa9',
         '&copy;': '\xc2\xa9',
         '&#170;': '\xc2\xaa',
         '&ordf;': '\xc2\xaa',
         '&#171;': '\xc2\xab',
         '&laquo;': '\xc2\xab',
         '&#172;': '\xc2\xac',
         '&not;': '\xc2\xac',
         '&#173;': ' ',
         '&shy;': '\xc2\xad ',
         '&#174;': '\xc2\xae',
         '&reg;': '\xc2\xae',
         '&#175;': '\xc2\xaf',
         '&macr;': '\xc2\xaf',
         '&#176;': '\xc2\xb0',
         '&deg;': '\xc2\xb0',
         '&#177;': '\xc2\xb1',
         '&plusmn;': '\xc2\xb1',
         '&#178;': '\xc2\xb2',
         '&sup2;': '\xc2\xb2',
         '&#179;': '\xc2\xb3',
         '&sup3;': '\xc2\xb3',
         '&#180;': '\xc2\xb4',
         '&acute;': '\xc2\xb4',
         '&#181;': '\xc2\xb5',
         '&micro;': '\xc2\xb5',
         '&#182;': '\xc2\xb6',
         '&para;': '\xc2\xb6',
         '&#183;': '\xc2\xb7',
         '&middot;': '\xc2\xb7',
         '&#184;': '\xc2\xb8',
         '&cedil;': '\xc2\xb8',
         '&#185;': '\xc2\xb9',
         '&sup1;': '\xc2\xb9',
         '&#186;': '\xc2\xba',
         '&ordm;': '\xc2\xba',
         '&#187;': '\xc2\xbb',
         '&raquo;': '\xc2\xbb',
         '&#188;': '\xc2\xbc',
         '&frac14;': '\xc2\xbc',
         '&#189;': '\xc2\xbd',
         '&frac12;': '\xc2\xbd',
         '&#190;': '\xc2\xbe',
         '&frac34;': '\xc2\xbe',
         '&#191;': '\xc2\xbf',
         '&iquest;': '\xc2\xbf',
         '&#192;': '\xc3\x80',
         '&Agrave;': '\xc3\x80',
         '&#193;': '\xc3\x81',
         '&Aacute;': '\xc3\x81',
         '&#194;': '\xc3\x82',
         '&Acirc;': '\xc3\x82',
         '&#195;': '\xc3\x83',
         '&Atilde;': '\xc3\x83',
         '&#196;': '\xc3\x84',
         '&Auml;': '\xc3\x84',
         '&#197;': '\xc3\x85',
         '&Aring;': '\xc3\x85',
         '&#198;': '\xc3\x86',
         '&AElig;': '\xc3\x86',
         '&#199;': '\xc3\x87',
         '&Ccedil;': '\xc3\x87',
         '&#200;': '\xc3\x88',
         '&Egrave;': '\xc3\x88',
         '&#201;': '\xc3\x89',
         '&Eacute;': '\xc3\x89',
         '&#202;': '\xc3\x8a',
         '&Ecirc;': '\xc3\x8a',
         '&#203;': '\xc3\x8b',
         '&Euml;': '\xc3\x8b',
         '&#204;': '\xc3\x8c',
         '&Igrave;': '\xc3\x8c',
         '&#205;': '\xc3\x8d',
         '&Iacute;': '\xc3\x8d',
         '&#206;': '\xc3\x8e',
         '&Icirc;': '\xc3\x8e',
         '&#207;': '\xc3\x8f',
         '&Iuml;': '\xc3\x8f',
         '&#208;': '\xc3\x90',
         '&ETH;': '\xc3\x90',
         '&#209;': '\xc3\x91',
         '&Ntilde;': '\xc3\x91',
         '&#210;': '\xc3\x92',
         '&Ograve;': '\xc3\x92',
         '&#211;': '\xc3\x93',
         '&Oacute;': '\xc3\x93',
         '&#212;': '\xc3\x94',
         '&Ocirc;': '\xc3\x94',
         '&#213;': '\xc3\x95',
         '&Otilde;': '\xc3\x95',
         '&#214;': '\xc3\x96',
         '&Ouml;': '\xc3\x96',
         '&#215;': '\xc3\x97',
         '&times;': '\xc3\x97',
         '&#216;': '\xc3\x98',
         '&Oslash;': '\xc3\x98',
         '&#217;': '\xc3\x99',
         '&Ugrave;': '\xc3\x99',
         '&#218;': '\xc3\x9a',
         '&Uacute;': '\xc3\x9a',
         '&#219;': '\xc3\x9b',
         '&Ucirc;': '\xc3\x9b',
         '&#220;': '\xc3\x9c',
         '&Uuml;': '\xc3\x9c',
         '&#221;': '\xc3\x9d',
         '&Yacute;': '\xc3\x9d',
         '&#222;': '\xc3\x9e',
         '&THORN;': '\xc3\x9e',
         '&#223;': '\xc3\x9f',
         '&szlig;': '\xc3\x9f',
         '&#224;': '\xc3\xa0',
         '&agrave;': '\xc3\xa0',
         '&#225;': '\xc3\xa1',
         '&aacute;': '\xc3\xa1',
         '&#226;': '\xc3\xa2',
         '&acirc;': '\xc3\xa2',
         '&#227;': '\xc3\xa3',
         '&atilde;': '\xc3\xa3',
         '&#228;': '\xc3\xa4',
         '&auml;': '\xc3\xa4',
         '&#229;': '\xc3\xa5',
         '&aring;': '\xc3\xa5',
         '&#230;': '\xc3\xa6',
         '&aelig;': '\xc3\xa6',
         '&#231;': '\xc3\xa7',
         '&ccedil;': '\xc3\xa7',
         '&#232;': '\xc3\xa8',
         '&egrave;': '\xc3\xa8',
         '&#233;': '\xc3\xa9',
         '&eacute;': '\xc3\xa9',
         '&#234;': '\xc3\xaa',
         '&ecirc;': '\xc3\xaa',
         '&#235;': '\xc3\xab',
         '&euml;': '\xc3\xab',
         '&#236;': '\xc3\xac',
         '&igrave;': '\xc3\xac',
         '&#237;': '\xc3\xad',
         '&iacute;': '\xc3\xad',
         '&#238;': '\xc3\xae',
         '&icirc;': '\xc3\xae',
         '&#239;': '\xc3\xaf',
         '&iuml;': '\xc3\xaf',
         '&#240;': '\xc3\xb0',
         '&eth;': '\xc3\xb0',
         '&#241;': '\xc3\xb1',
         '&ntilde;': '\xc3\xb1',
         '&#242;': '\xc3\xb2',
         '&ograve;': '\xc3\xb2',
         '&#243;': '\xc3\xb3',
         '&oacute;': '\xc3\xb3',
         '&#244;': '\xc3\xb4',
         '&ocirc;': '\xc3\xb4',
         '&#245;': '\xc3\xb5',
         '&otilde;': '\xc3\xb5',
         '&#246;': '\xc3\xb6',
         '&ouml;': '\xc3\xb6',
         '&#247;': '\xc3\xb7',
         '&divide;': '\xc3\xb7',
         '&#248;': '\xc3\xb8',
         '&oslash;': '\xc3\xb8',
         '&#249;': '\xc3\xb9',
         '&ugrave;': '\xc3\xb9',
         '&#250;': '\xc3\xba',
         '&uacute;': '\xc3\xba',
         '&#251;': '\xc3\xbb',
         '&ucirc;': '\xc3\xbb',
         '&#252;': '\xc3\xbc',
         '&uuml;': '\xc3\xbc',
         '&#253;': '\xc3\xbd',
         '&yacute;': '\xc3\xbd',
         '&#254;': '\xc3\xbe',
         '&thorn;': '\xc3\xbe',
         '&#255;': '\xc3\xbf',
         '&yuml;': '\xc3\xbf',
         '&#133;': '...',
         '&#151;': '-',
         '<br><br>': ' ',
         '<br />': '',
         '\r': '',
         '\n': '',
         '  ': ' ',
         '&ndash;': '\xe2\x80\x93',
         '</i>': '',
         '<i>': '',
         '<span>': '',
         '</span>': ''}
        for i in range(len(symbols_to_remove)):
            processingstring = string.replace(processingstring, symbols_to_remove.items()[i][0], symbols_to_remove.items()[i][1])

        return processingstring
    except:
        return ''


def singleValue(content, matchstring):
    result = ''
    regexp = re.compile(matchstring, re.DOTALL)
    result = regexp.search(content)
    if result != None:
        result = result.group(1)
        return result
    else:
        return ''


def multiValue(content, matchstring, matchstring2):
    result = ''
    regexp = re.compile(matchstring, re.DOTALL)
    result = regexp.search(content)
    regexp = re.compile(matchstring2, re.DOTALL)
    result = regexp.finditer(result.group(0))
    j = 0
    retList = []
    for i in result:
        if i.group(1):
            retList.append(i.group(1))
        else:
            retList.append(i.group(0))
        j += 1

    result = retList
    return result


def search_title(title):
    yearitem = ''
    titleitem = ''
    iditem = ''
    genres = ''
    search = ''
    title = title.replace(' ', '%20').decode('utf8')
    encoded_args = urllib.quote(title.encode('cp1251'))
    url = 'http://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s' % encoded_args
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    content = watchvideopage.read().decode('cp1251').encode('utf-8')
    watchvideopage.close()
    search_results = []
    content_results = content[content.find('\xd0\xa1\xd0\xba\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb5 \xd0\xb2\xd1\x81\xd0\xb5\xd0\xb3\xd0\xbe, \xd0\xb2\xd1\x8b \xd0\xb8\xd1\x89\xd0\xb5\xd1\x82\xd0\xb5:'):content.find('search_results search_results_last')]
    if content_results:
        results = CrewRoleList(content_results)
        yearitems = re.compile('<span class="year">(.*?)</span>').findall(content_results)
        titleitems = re.compile('<p class="name"><a href="/film/.*?/sr/1/" .*? data-type=".*?">(.*?)</a> <span class="year">.*?</span></p>').findall(content_results)
        iditems = re.compile('<p class="name"><a href="/film/.*?/sr/1/" .*? data-id="(.*?)" data-type=".*?">.*?</a> <span class="year">.*?</span></p>').findall(content_results)
        genres = re.compile('<span class="genres">(.*?)</span>').findall(results)
        for titleitem in titleitems:
            search_results.append(normilize_string(titleitem))

        i = 0
        for yearitem in yearitems:
            if i < len(yearitems):
                search_results[i] = search_results[i] + '(' + normilize_string(yearitem) + ' \xd0\xb3\xd0\xbe\xd0\xb4),'
            i += 1

        l = 0
        for iditem in iditems:
            if l < len(iditems):
                search_results[l] = search_results[l] + '\n genres:' + genres[l] + 'end' + '\n\n' + 'id:' + iditem.strip() + 'end'
            l += 1

    else:
        try:
            genres = ','.join(multiValue(content, '<tr><td class="type">\xd0\xb6\xd0\xb0\xd0\xbd\xd1\x80</td>(.*?)</tr>', '<a href=".*?>(.*?)</a>'))
            genres = '\n genres:' + genres + 'end'
        except:
            genres = '\n genres:end'

        try:
            titleitem = normilize_string(singleValue(content, '<h1 class="moviename-big" itemprop="name">(.*?)</h1>'))
        except:
            titleitem = ''

        try:
            yearitem = ','.join(multiValue(content, '<td class="type">\xd0\xb3\xd0\xbe\xd0\xb4</td>(.*?)</div></td>', '<a href=".*?" title=".*?">(.*?)</a>'))
            yearitem = '(%s \xd0\xb3\xd0\xbe\xd0\xb4),' % yearitem
        except:
            yearitem = ''

        try:
            iditem = singleValue(content, '<link rel="canonical" href="http://www.kinopoisk.ru/film/(.*?)/" />')
            iditem = '\n\nid:%send' % iditem
        except:
            iditem = '\n\nid: end'

        search = '%s%s%s%s' % (titleitem,
         yearitem,
         genres,
         iditem)
        search_results.append(search)
    return search_results


def CrewRoleList2(file):
    if file:
        return file.replace('<br />', '').replace('     ', '').replace('\n', '').replace('<b>', '').replace('</b>', '')


def CrewRoleList(file):
    if file:
        return file.replace('<br />', '<span class="genres">').replace('     ', '').replace('\n', '').replace('\t', '')


def search_title2(title):
    yearitem = ''
    titleitem = ''
    iditem = ''
    rating = ''
    director = ''
    titleengle = ''
    countri = ''
    iditem = ''
    search = ''
    runtime = ''
    time = ''
    title = title.replace(' ', '%20').decode('utf8')
    encoded_args = urllib.quote(title.encode('cp1251'))
    url = 'http://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s' % encoded_args
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    content = watchvideopage.read().decode('cp1251').encode('utf-8')
    watchvideopage.close()
    search_results = []
    content_results = content[content.find('\xd0\xa1\xd0\xba\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb5 \xd0\xb2\xd1\x81\xd0\xb5\xd0\xb3\xd0\xbe, \xd0\xb2\xd1\x8b \xd0\xb8\xd1\x89\xd0\xb5\xd1\x82\xd0\xb5:'):content.find('search_results search_results_last')]
    if content_results:
        titleitems = re.compile('<p class="name"><a href="/level/1/film/.*?/sr/1/" .*? data-type=".*?">(.*?)</a> <span class="year">.*?</span></p>').findall(content_results)
        titleengles = re.compile('<span class="gray">(.*?)</span>').findall(content_results)
        directors = re.compile('<span class="gray">.*? <i class="director">.*? <a class=".*?" .*? data-type=".*?">(.*?)</a>').findall(content_results)
        countris = re.compile('<span class="gray">(.*?) <i class="director">.*? <a class=".*?" .*? data-type=".*?">.*?</a>').findall(content_results)
        iditems = re.compile('<p class="name"><a href="/level/1/film/(.*?)/sr/1/" .*? data-type="film">.*?</a> <span class="year">.*?</span></p>').findall(content_results)
        ratings = re.compile('<div class="rating.*?>(.*?)</div>').findall(content_results)
        for titleitem in titleitems:
            search_results.append(normilize_string(titleitem.replace('</a>', '').replace(' <span class="year">', '(').replace('</span>', ' \xd0\xb3\xd0\xbe\xd0\xb4),').replace('</p>', '')))

        k = 0
        for titleengle in titleengles:
            if titleengle == '':
                titleengle = '\xd0\x9d\xd0\xb5\xd1\x82 \xd0\xbd\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f'
            if k < len(titleengles):
                search_results[k] = search_results[k] + '\n' + normilize_string(titleengle)
            k += 1

        d = 0
        for director in directors:
            if d < len(directors):
                search_results[d] = search_results[d] + '\n' + countris[d] + '\xd1\x80\xd0\xb5\xd0\xb6. ' + normilize_string(director)
            d += 1

        l = 0
        for iditem in iditems:
            if l < len(iditems):
                search_results[l] = search_results[l] + '\n\n' + 'id:' + iditem + 'end'
            l += 1

        e = 0
        for rating in ratings:
            if e < len(ratings):
                search_results[e] = search_results[e] + '\n' + 'rating:' + rating + 'ends'
            e += 1

    else:
        try:
            titleitem = normilize_string(singleValue(content, '<h1 class="moviename-big" itemprop="name">(.*?)</h1>'))
        except:
            titleitem = ''

        try:
            director = normilize_string(','.join(multiValue(content, '<tr><td class="type">\xd1\x80\xd0\xb5\xd0\xb6\xd0\xb8\xd1\x81\xd1\x81\xd0\xb5\xd1\x80</td>(.*?)</tr>', '<a href=".*?>(.*?)</a>')))
            director = '\xd1\x80\xd0\xb5\xd0\xb6. %s' % director
        except:
            director = ''

        try:
            countri = ','.join(multiValue(content, '<td class="type">\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb0</td>(.*?)</tr>', '<a href=".*?>(.*?)</a>'))
            countri = '\n%s ,' % countri
        except:
            countri = ''

        try:
            time = string.split(singleValue(content, '<td class="time" id="runtime">(.*?)</td>'))
            runtime = time[0] + ' \xd0\xbc\xd0\xb8\xd0\xbd.'
        except:
            runtime = ''

        try:
            yearitem = ','.join(multiValue(content, '<td class="type">\xd0\xb3\xd0\xbe\xd0\xb4</td>(.*?)</div></td>', '<a href=".*?" title=".*?">(.*?)</a>'))
            yearitem = '(%s \xd0\xb3\xd0\xbe\xd0\xb4),' % yearitem
        except:
            yearitem = ''

        try:
            titleengle = normilize_string(singleValue(content, '<span itemprop="alternativeHeadline">(.*?)</span>'))
            titleengle = '\n%s, ' % titleengle
        except:
            titleengle = ''

        try:
            rating = singleValue(content, '<div class="div1"><meta itemprop="ratingValue" content="(.*?)" />')
            rating = '\nrating:%sends' % rating
        except:
            rating = '\nrating:  ends'

        try:
            iditem = singleValue(content, '<link rel="canonical" href="http://www.kinopoisk.ru/film/(.*?)/" />')
            iditem = '\n\nid:%send' % iditem
        except:
            iditem = '\n\nid: end'

        search = '%s%s%s%s%s%s%s%s' % (titleitem,
         yearitem,
         titleengle,
         runtime,
         countri,
         director,
         iditem,
         rating)
        search_results.append(search)
    return search_results


def search_data(id):
    url = 'http://www.kinopoisk.ru/level/1/film/' + id
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data = watchvideopage.read().decode('cp1251').encode('utf-8')
    content_results = '%s' % data.replace('     ', '').replace('\n', '').replace('\t', '')
    watchvideopage.close()
    try:
        filmdata = {'title': '',
         'countries': '',
         'year': '',
         'directors': '',
         'cast': '',
         'genre': '',
         'user_rating': '',
         'rating_count': '',
         'movie_rating': '',
         'plot': '',
         'runtime': ''}
        try:
            filmdata['title'] = normilize_string(singleValue(data, '<title>(.*?)</title>'))
        except:
            filmdata['title'] = ''

        try:
            filmdata['directors'] = normilize_string(','.join(multiValue(data, '<tr><td class="type">\xd1\x80\xd0\xb5\xd0\xb6\xd0\xb8\xd1\x81\xd1\x81\xd0\xb5\xd1\x80</td>(.*?)</tr>', '<a href=".*?>(.*?)</a>')))
        except:
            filmdata['directors'] = ''

        try:
            filmdata['countries'] = ','.join(multiValue(data, '<td class="type">\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb0</td>(.*?)</tr>', '<a href=".*?>(.*?)</a>'))
        except:
            filmdata['countries'] = ''

        try:
            filmdata['year'] = ','.join(multiValue(data, '<td class="type">\xd0\xb3\xd0\xbe\xd0\xb4</td>(.*?)</div></td>', '<a href=".*?" title=".*?">(.*?)</a>'))
        except:
            filmdata['year'] = ''

        try:
            filmdata['genre'] = ','.join(multiValue(data, '<tr><td class="type">\xd0\xb6\xd0\xb0\xd0\xbd\xd1\x80</td>(.*?)</tr>', '<a href=".*?>(.*?)</a>'))
        except:
            filmdata['genre'] = ''

        try:
            filmdata['user_rating'] = singleValue(content_results, '<div class="div1"><meta itemprop="ratingValue" content="(.*?)" />')
        except:
            filmdata['user_rating'] = ''

        try:
            filmdata['rating_count'] = normilize_string(singleValue(data, '<span class="ratingCount">(.*?)</span>'))
        except:
            filmdata['rating_count'] = ''

        try:
            filmdata['plot'] = normilize_string(singleValue(data, '<tr><td colspan=3 style="padding: 10px.*?description">(.*?)</div></span>'))
        except:
            filmdata['plot'] = ''

        try:
            runtime = string.split(singleValue(data, '<td class="time" id="runtime">(.*?)</td>'))
            filmdata['runtime'] = runtime[0]
        except:
            filmdata['runtime'] = ''

        try:
            filmdata['cast'] = normilize_string(','.join(multiValue(data, '<h4>\xd0\x92 \xd0\xb3\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd1\x8b\xd1\x85 \xd1\x80\xd0\xbe\xd0\xbb\xd1\x8f\xd1\x85:</h4>(.*?)</a></li></ul>', '<a href="/name/.*?/">(.*?)</a>')))
        except:
            filmdata['cast'] = ''

        try:
            movierating = string.split(singleValue(data, '<td class="type">рейтинг MPAA</td>.*?<img src.*?alt=(.*?) border=0>'))
            if len(movierating) > 0:
                filmdata['movie_rating'] = movierating[1]
            else:
                filmdata['movie_rating'] = ''
        except:
            filmdata['movie_rating'] = ''

        return filmdata
    except:
        print_exception(traceback.format_exc())


def search_comets(id):
    url = 'http://www.kinopoisk.ru/level/1/film/' + id
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    content = watchvideopage.read().decode('cp1251').encode('utf-8')
    watchvideopage.close()
    search_results = []
    content_results = content[content.find('<p class="more_random">'):content.find('\xd0\x94\xd0\xbb\xd1\x8f \xd1\x82\xd0\xbe\xd0\xb3\xd0\xbe \xd1\x87\xd1\x82\xd0\xbe\xd0\xb1\xd1\x8b \xd0\xb4\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c \xd1\x80\xd0\xb5\xd1\x86\xd0\xb5\xd0\xbd\xd0\xb7\xd0\xb8\xd1\x8e \xd0\xbd\xd0\xb0 \xd1\x84\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbc, \xd0\xbd\xd0\xb5\xd0\xbe\xd0\xb1\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xbe')]
    if content_results:
        results = CrewRoleList2(content_results)
        names = normilize_string(singleValue(results, '<p class="profile_name"><s></s><a href=".*?" itemprop="name">(.*?)</a></p>'))
        titleitems = normilize_string(singleValue(results, '<span class="_reachbanner_" itemprop="reviewBody">(.*?)</span></p> </div>'))
        iditems = normilize_string(singleValue(results, '<p class="sub_title" id=".*?">(.*?)</p>'))
        search = '%s\n\n%s\n\n%s' % (names, iditems, titleitems)
        search_results.append(search)
    return search_results


def search_poster(id):
    url = 'http://www.kinopoisk.ru/level/17/film/%s' % id
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data = watchvideopage.read().decode('cp1251').encode('utf-8')
    coveritems = []
    watchvideopage.close()
    if '<table class="fotos' in data:
        coveritems = multiValue(data, '<table class="fotos.*?">(.*?)</table>', '<a href="(.*?)">')
        Coverart = coveritems[0]
        url2 = 'http://www.kinopoisk.ru%s' % Coverart
        watchrequest2 = Request(url2, None, std_headers)
        try:
            watchvideopage2 = urlopen2(watchrequest2)
        except (URLError, HTTPException, socket.error) as err:
            print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

        data2 = watchvideopage2.read().decode('cp1251').encode('utf-8')
        coveritem = ''
        coveritem = singleValue(data2, '<img style=".*?" id="image" src="(.*?)".*?/>')
        watchvideopage2.close()
    else:
        coveritem = 'None'
    return coveritem


def poster_save(id):
    url2 = 'http://www.kinopoisk.ru%s' % id
    watchrequest2 = Request(url2, None, std_headers)
    try:
        watchvideopage2 = urlopen2(watchrequest2)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data2 = watchvideopage2.read().decode('cp1251').encode('utf-8')
    coveritem = ''
    coveritem = singleValue(data2, '<img style=".*?" id="image" src="(.*?)".*?/>')
    watchvideopage2.close()
    return coveritem


def poster_viem(id):
    url = 'http://www.kinopoisk.ru/level/17/film/%s' % id
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data = watchvideopage.read().decode('cp1251').encode('utf-8')
    search_results = []
    watchvideopage.close()
    if '<table class="fotos' in data:
        content_results = singleValue(data, '<table class="fotos.*?">(.*?)</table>')
        if content_results:
            results = CrewRoleList3(content_results)
            idposters = re.compile('<a href="(.*?)" target="_blank" title="\xd0\x9e\xd1\x82\xd0\xba\xd1\x80\xd1\x8b\xd1\x82\xd1\x8c \xd0\xb2 \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xbc \xd0\xbe\xd0\xba\xd0\xbd\xd0\xb5"></a>').findall(content_results)
            imageslinks = re.compile('<img  src="(.*?)".*?/></a>').findall(content_results)
            imagessaizes = re.compile('<span class="genre">(.*?)</span>').findall(results)
            for imagessaize in imagessaizes:
                search_results.append('size:' + imagessaize)

            i = 0
            for idposter in idposters:
                if i < len(idposters):
                    search_results[i] = search_results[i] + '\n\n (' + idposter + ')'
                i += 1

            l = 0
            for imageslink in imageslinks:
                if l < len(imageslinks):
                    search_results[l] = search_results[l] + '\n link:' + imageslink + 'end'
                l += 1

    return search_results


def search_tmbd(title):
    url = 'http://www.themoviedb.org/search?query=%s' % title
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data = watchvideopage.read()
    search_results = []
    watchvideopage.close()
    if '<div class="search_results movie ">' in data:
        content_results = singleValue(data, '<div class="search_results movie ">(.*?)<div class="search_results collection hide">')
        if content_results:
            iditems = re.compile('<a id=".*?" class="result" href="(.*?)" title=".*?" alt=".*?">').findall(content_results)
            years = re.compile('<span class="release_date"> (.*?) <span class=".*?"></span></span>').findall(content_results)
            directors = re.compile('<span class="genres">(.*?)</span>').findall(content_results)
            images = re.compile('<img class="poster lazyload" data-src="(.*?)" .*? alt=".*?">').findall(content_results)
            titleitems = re.compile('<a id=".*?" class="result" href=".*?" title="(.*?)" alt=".*?">').findall(content_results)
            for titleitem in titleitems:
                search_results.append(titleitem)

            d = 0
            for director in directors:
                if d < len(directors):
                    search_results[d] = search_results[d] + '\n year: ' + years[d] + '\n \xd1\x80\xd0\xb5\xd0\xb6. ' + director
                d += 1

            l = 0
            for iditem in iditems:
                if l < len(iditems):
                    search_results[l] = search_results[l] + '\n' + 'id:' + iditem + 'end'
                l += 1

            e = 0
            for image in images:
                if e < len(images):
                    search_results[e] = search_results[e] + '\n' + 'image:' + image + 'ends'
                e += 1

    return search_results


def poster_viemtmbd(id):
    url = 'http://www.themoviedb.org%s' % id
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data = watchvideopage.read()
    search_results = []
    watchvideopage.close()
    if '<div id="images">' in data:
        content_results = singleValue(data, '<div id="images">(.*?)</div>')
        if content_results:
            idposters = re.compile('<img itemprop=".*?" class=".*?" id=".*?" src="(.*?)" width=".*?" height=".*?" />').findall(content_results)
            imagessaizes = re.compile('<img itemprop=".*?" class=".*?" id="(.*?)" src=".*?" width=".*?" height=".*?" />').findall(content_results)
            for imagessaize in imagessaizes:
                search_results.append('image:' + imagessaize)

            l = 0
            for idposter in idposters:
                if l < len(idposters):
                    search_results[l] = search_results[l] + '\n link:' + idposter + 'end'
                l += 1

    return search_results


def CrewRoleList3(file):
    if file:
        return file.replace('<b><i>', '<span class="genre">').replace('</i>', '</span>').replace('&times;', 'x')


def search_postermp3(url):
    watchrequest = Request(url, None, std_headers)
    try:
        watchvideopage = urlopen2(watchrequest)
    except (URLError, HTTPException, socket.error) as err:
        print('[Kinopoisk] Error: Unable to retrieve page - Error code: ', str(err))

    data = watchvideopage.read()
    search_results = []
    cover = ''
    watchvideopage.close()
    if 'src="' in data:
        coveritems = re.compile('src="(.*?)"').findall(data)
        for coveritem in coveritems:
            if 'http://' in coveritem:
                if '&imgurl=' in coveritem:
                    search_results.append(singleValue(coveritem, '&imgurl=(.*?)&w='))
                else:
                    search_results.append(coveritem)

    return search_results
