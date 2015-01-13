import requests


def download_url(url):
    """ Download a url, returning the content as a unicode string. """
    r = requests.get(url)
    return r.text
