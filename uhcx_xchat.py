"""
uh.cx
X-Chat Version

@homepage: http://uh.cx
@copyright: Copyright (C) 2015 J. Boehm
"""

__module_name__ = "uh.cx"
__module_version__ = "0.2"
__module_description__ = "Make a shortened URL with uh.cx and post it to a channel or user."
__module_author__ = "uh.cx (J. Boehm)"

import urllib
import traceback
import json
import urllib2

import xchat


class Manager:
    _url = 'http://uh.cx/api/create'

    def __init__(self):
        pass

    class Link:
        def __init__(self):
            pass

        url_original = ''
        url_redirect = ''
        url_preview = ''
        qr_redirect = ''
        qr_preview = ''

    class InvalidResponseException(Exception):
        pass

    class CouldNotCreateLinkException(Exception):
        pass

    class ResponseValidator:
        _keys = ['QrDirect', 'QrPreview', 'UrlDirect', 'UrlOriginal', 'UrlPreview']

        def __init__(self):
            pass

        @staticmethod
        def check(response):
            for key in Manager.ResponseValidator._keys:
                if key not in response:
                    return False

            return True

    @staticmethod
    def create(url):
        try:
            request = urllib2.Request(Manager._url, urllib.urlencode({'url': url}))
            response = urllib2.urlopen(request)
            response_data = json.loads(response.read())
        except urllib2.HTTPError:
            raise Manager.InvalidResponseException()

        if not Manager.ResponseValidator.check(response_data):
            raise Manager.InvalidResponseException()

        link = Manager.Link()
        link.qr_preview = response_data['QrPreview']
        link.qr_redirect = response_data['QrDirect']
        link.url_original = response_data['UrlOriginal']
        link.url_preview = response_data['UrlPreview']
        link.url_redirect = response_data['UrlDirect']

        return link


def on_uhcx(word, word_eol, userdata):
    if len(word) < 2:
        print 'Usage: /uhcx http://your.long.url/'
    else:
        try:
            url = word[1]
            o = Manager.create(url)
            xchat.command('SAY ' + o.url_redirect)

        except Manager.InvalidResponseException:
            print 'An error occured. Did you try to shorten an invalid URL?'
        except:
            print traceback.print_exc()
            print ''
            print 'An unknown error occurred! I cannot create your url. Sorry!'

    return xchat.EAT_ALL


xchat.hook_command('uhcx', on_uhcx, help='/uhcx http://your.long.url/')
