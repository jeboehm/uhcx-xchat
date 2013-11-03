"""
uh.cx
API-Client X-Chat

@homepage: http://uh.cx
@copyright: Copyright (C) 2012 J. Boehm
"""

__module_name__ = "uh.cx"
__module_version__ = "0.1"
__module_description__ = "Make a shortened URL with uh.cx and post it to a channel or user."
__module_author__ = "uh.cx (J. Boehm)"

import json
import urllib
import urllib2
import xchat

"""
Usage:

/uhcx http://your.long.url/

This will post your shortened URL to the user or channel.

"""
class uhcx:
    __apiurl = "http://uh.cx/api"
    
    @staticmethod 
    def __sendRequestToApi(longurl):
        apiurl = uhcx.__apiurl + "/create/json"
        post = {"url" : longurl}
        
        data = urllib.urlencode(post)
        req = urllib2.Request(apiurl, data)
        response = urllib2.urlopen(req)
        
        return response.read()
    
    @staticmethod
    def __decodeApiResponse(response):
        decoded = json.loads(response)
        
        if not decoded['UrlDirect'] or not decoded['UrlPreview'] \
        or not decoded['QrDirect'] or not decoded['QrPreview']:
            raise Exception("Invalid API Response!")

        return decoded
        
    @staticmethod
    def create(longurl):
        response = uhcx.__sendRequestToApi(longurl)
        decoded = uhcx.__decodeApiResponse(response)
        
        ob = uhcx_return(decoded)
        
        return ob
        

class uhcx_return:
    __prependQr = "http://uh.cx/"
    __response = []
    
    def __init__(self, response):
        if not response['UrlDirect'] or not response['UrlPreview'] \
        or not response['QrDirect'] or not response['QrPreview']:
            raise Exception("Invalid API Response!")
        
        self.__response = response
        
    def getShortUrl(self):
        return self.__response['UrlDirect']

    def getPreviewUrl(self):
        return self.__response['UrlPreview']
    
    def getQrShort(self):
        return self.__prependQr + self.__response['QrDirect']
    
    def getQrPreview(self):
        return self.__prependQr + self.__response['QrPreview']
    

def onUhcx(word, word_eol, userdata):
    if len(word) < 2:
        print "Usage: /uhcx http://your.long.url/"
    else:
        try:
            o = uhcx.create(word[1])
            xchat.command("SAY " + o.getShortUrl())
        except:
            print "An error occurred! I can't create your url. Sorry!"
        
    return xchat.EAT_ALL

xchat.hook_command("uhcx", onUhcx, help="/uhcx http://your.long.url/")
        
