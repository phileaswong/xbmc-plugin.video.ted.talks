import unittest
import subtitles_scraper
import urllib
import tempfile
from BeautifulSoup import MinimalSoup

def get_talk_1253():
    '''
    Return soup for an arbitrary fixed talk.
    '''
    return MinimalSoup(urllib.urlopen('http://www.ted.com/talks/richard_wilkinson.html').read())

class TestSubtitlesScraper(unittest.TestCase):
    
    def test_format_time(self):
        self.assertEqual('00:00:00,000', subtitles_scraper.format_time(0))
        self.assertEqual('03:25:45,678', subtitles_scraper.format_time(12345678))

    def test_get_languages(self):
        languages = '%5B%7B%22LanguageCode%22%3A%22sq%22%2C%22OldLanguageCode%22%3A%22alb%22%2C%22Name%22%3A%22Albanian%22%2C%22Description%22%3Anull%2C%22CommunityUrl%22%3Anull%2C%22TranslationCount%22%3A288%2C%22DotsubOnly%22%3Afalse%2C%22CreatedAt%22%3A%222009-05-12+22%3A17%3A26%22%2C%22UpdatedAt%22%3A%222012-03-26+18%3A27%3A09%22%7D%2C%7B%22LanguageCode%22%3A%22ar%22%2C%22OldLanguageCode%22%3A%22ara%22%2C%22Name%22%3A%22Arabic%22%2C%22Description%22%3Anull%2C%22CommunityUrl%22%3Anull%2C%22TranslationCount%22%3A1086%2C%22DotsubOnly%22%3Afalse%2C%22CreatedAt%22%3A%222009-05-12+22%3A17%3A26%22%2C%22UpdatedAt%22%3A%222012-03-26+18%3A26%3A46%22%7D%2C%'
        self.assertEquals(['sq', 'ar'], subtitles_scraper.get_languages(languages))

    def test_get_flashvars(self):
        soup = get_talk_1253()
        # This should be the language list once we get back the point of parsing the languages param
        # expected = ['sq', 'ar', 'hy', 'bg', 'ca', 'zh-cn', 'zh-tw', 'hr', 'cs', 'da', 'nl', 'en', 'fr', 'ka', 'de', 'el', 'he', 'hu', 'id', 'it', 'ja', 'ko', 'fa', 'pl', 'pt-br', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'th', 'tr', 'uk', 'vi']
        flashvars = subtitles_scraper.get_flashvars(soup)
        self.assertTrue('languages' in flashvars) # subtitle languages 
        self.assertTrue('introDuration' in flashvars) # TED intro, need to offset subtitles with this
        self.assertTrue('ti' in flashvars) # talk ID
        
    def test_get_flashvars_not_there(self):
        soup = MinimalSoup('<html><head/><body><script>Not much here</script></body></html>')
        try:
            subtitles_scraper.get_flashvars(soup)
            self.fail()
        except Exception, e:
            self.assertEqual('Could not find flashVars', e.args[0])
        
    def test_get_subtitles(self):
        subs = subtitles_scraper.get_subtitles('1253', 'en')
        self.assertEqual(385, len(subs))
    
    def test_get_subtitles_for_url(self):
        json_subs = '{"captions":[{"content":"What","startTime":0,"duration":3000,"startOfParagraph":false},{"content":"Began","startTime":3000,"duration":4000,"startOfParagraph":false}]}'
        subs_file = tempfile.NamedTemporaryFile()
        try:  
            subs_file.write(json_subs)
            subs_file.flush()
            subs = subtitles_scraper.get_subtitles_for_url(subs_file.name)
        finally:
            subs_file.close()
        self.assertEqual([{'duration': 3000, 'start': 0, 'content': 'What'}, {'duration': 4000, 'start': 3000, 'content': 'Began'}], subs)
    