from __future__ import print_function
from Components.config import config
from Components.PluginComponent import plugins
from Plugins.Plugin import PluginDescriptor

configs = None


def setLocale(lng):
    global configs
    configs = {}
    configs['locale'] = lng


def getLocale():
    return configs['locale']


def decodeCertification(releases):
    cert = None
    if 'US' in releases:
        cert = releases['US'].certification
    certification = {'G': 'VSR-0',
     'PG': 'VSR-6',
     'PG13': 'VSR-12',
     'PG-13': 'VSR-12',
     'R': 'VSR-16',
     'NC-13': 'VSR-18',
     'NC17': 'VSR-18'}
    if cert in certification:
        return certification[cert]


def nextImageIndex(movie):
    if len(movie['images']) > 1:
        item = movie['images'].pop(0)
        movie['images'].append(item)


def prevImageIndex(movie):
    if len(movie['images']) > 1:
        item = movie['images'].pop(-1)
        movie['images'].insert(0, item)


def init_tmdb3(alternative_lang=None):
    import tmdb3
    tmdb3.set_key('1f834eb425728133b9a2c1c0c82980eb')
    tmdb3.set_cache('null')
    lng = alternative_lang or config.plugins.tmbd.locale.value
    if lng == 'en':
        tmdb3.set_locale(lng, 'US')
    elif lng == 'el':
        tmdb3.set_locale(lng, 'GR')
    elif lng == 'cs':
        tmdb3.set_locale(lng, 'CZ')
    elif lng == 'da':
        tmdb3.set_locale(lng, 'DK')
    elif lng == 'uk':
        tmdb3.set_locale('en', 'GB')
    elif lng == 'fy':
        tmdb3.set_locale(lng, 'NL')
    else:
        try:
            tmdb3.set_locale(lng, lng.upper())
        except:
            tmdb3 = None
    return tmdb3


def main():
    setLocale('de')
    tmdb3 = init_tmdb3()
    res = tmdb3.searchMovie('F\xc3\xbcr immer Liebe')
    print(res)
    movie = res[0]
    print(movie.title)
    print(movie.releasedate.year)
    print(movie.overview)
    for p in movie.posters:
        print(p)

    for p in movie.backdrops:
        print(p)

    p = movie.poster
    print(p)
    print(p.sizes())
    print(p.geturl())
    print(p.geturl('w185'))
    p = movie.backdrop
    print(p)
    print(p.sizes())
    print(p.geturl())
    print(p.geturl('w300'))
    crew = [x.name for x in movie.crew if x.job == 'Director']
    print(crew)
    crew = [x.name for x in movie.crew if x.job == 'Author']
    print(crew)
    crew = [x.name for x in movie.crew if x.job == 'Producer']
    print(crew)
    crew = [x.name for x in movie.crew if x.job == 'Director of Photography']
    print(crew)
    crew = [x.name for x in movie.crew if x.job == 'Editor']
    print(crew)
    crew = [x.name for x in movie.crew if x.job == 'Production Design']
    print(crew)
    cast = [x.name for x in movie.cast]
    print(cast)
    genres = [x.name for x in movie.genres]
    print(genres)
    studios = [x.name for x in movie.studios]
    print(studios)
    countries = [x.name for x in movie.countries]
    print(countries)


if __name__ == '__main__':
    main()
