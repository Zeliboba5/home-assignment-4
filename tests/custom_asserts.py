from urlparse import urlparse


class CustomAsserts:
    def __init__(self):
        pass

    def assertDomainEqual(self, full_url, expected_url):
        full_url = urlparse(full_url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=full_url)
        if domain != expected_url:
            raise AssertionError('expected_url not equal domain from full_url')
        return True

    def assertNewsChangeClass(self, blocks_number, news_form, chosen_block_class, not_chosen_block_class):
        for i in range(2, blocks_number + 1):  # starts from 2 because of unique main page layout
            if (news_form.get_news_block_classes(i) != chosen_block_class):
                raise AssertionError('news_form.get_news_block_classes(i) != chosen_block_class')

            news_form.click_news_block_button(i)

            if (news_form.get_news_block_classes(i) != not_chosen_block_class):
                raise AssertionError('news_form.get_news_block_classes(i) != not_chosen_block_class')
