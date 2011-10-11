# -*- coding: utf-8 -*-

"""
    MoinMoin - yuml
    Inspired by GoogleChart.py (http://moinmo.in/ParserMarket/GoogleChart)

    This parser creates a UML diagram using a yuml server, using
    the API described at http://yuml.me

    Configuration:
    - place in the data/plugin/parser directory of the moinmoin storage directory
    - restart server (if necessary, see http://moinmo.in/MoinDev/PluginConcept)

    Example usage:
    {{{
    #!yuml
    # Cool UML Diagram
    [Customer]+1->*[Order]
    [Order]++1-items >*[LineItem]
    [Order]-0..1>[PaymentMethod]
    }}}

    Edit the variable yuml_url to point to the required server, and the proxies dictionary to any necessary proxies

    v0.1: 30-Sep-2011.  Basic implementation displaying PNG

    @license: GNU GPL
"""
import sys
import urllib
import re

Dependencies = ["page"]

# replace with your local yuml and proxy details
yuml_url = "http://yuml.me"
#proxies = {'http': 'http://example.com:8080'}
proxies = {}


def createYumlUrl(raw_text):
    """Returns a URL encoding the requested diagram.  Comment lines are excluded."""
    lines = raw_text.split("\n")
    uml = ", ".join([l for l in lines if l[0] != '#'])
    url = "%s/diagram/smart/class/%s" % (yuml_url, uml)
    return url

class Parser:
    """ yuml parser """
    def __init__(self, raw, request, **kw):
        self.pagename      = request.page.page_name
        self.request       = request
        self.formatter     = request.formatter
        self.raw           = raw
        self.init_settings = True

        if 'debug' in kw['format_args']:
            self.debug = True

    def render(self, formatter):
        from MoinMoin.action import cache

        # checks if initializing of all attributes in __init__ was done
        if not self.init_settings:
            return

        # check if diagram on this page has been rendered before
        key = cache.key(self.request, itemname=self.pagename, content=self.raw)
        if not cache.exists(self.request, key):
            image = urllib.urlopen(createYumlUrl(self.raw), proxies=proxies)
            cache.put(self.request, key, image.read(), content_type="image/png")

        return formatter.image(src=cache.url(self.request, key), alt=self.raw)

        #return formatter.image(src=createYumlUrl(self.raw), alt=self.raw)


    def format(self, formatter):
        """ parser output """
        # checks if initializing of all attributes in __init__ was done
        if self.init_settings:
            self.request.write(self.formatter.div(1, css_class="yuml"))
            self.request.write(self.render(formatter))
            self.request.write(self.formatter.div(0))



