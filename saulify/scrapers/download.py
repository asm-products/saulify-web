import requests


def download_url(url):
    """ Download a url, returning the content as a unicode string. """
    response = requests.get(url)
    content_type = response.headers['content-type']
    return (response.text, content_type)
