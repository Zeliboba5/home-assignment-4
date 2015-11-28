from urlparse import urlparse

class CustomAsserts:
    def __init__(self):
        pass

    def assertDomainEqual(self, full_url, expected_url):
    	full_url = urlparse(full_url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=full_url)
        if domain != expected_url:
            raise AssertionError('expected_url not equal domain from full_url')
        return true
