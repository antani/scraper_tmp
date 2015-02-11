__author__ = 'vantani'

from urlparse import urlparse
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

def clean_words(title):
    cleanded_title = ' '.join([word for word in title.split() if word not in cachedStopWords])
    return cleanded_title

def is_url(url):
    flag=False
    if url:
        o = urlparse(url.strip())
        if o.scheme in ['http','https']:
            flag=True
        else:
            flag=False
    else:
        flag=False
    #print" Is Valid URL : ", url, flag
    return flag
