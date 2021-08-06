import re


def removeComments(text):
    if str(type(text)) == '<class \'str\'>':
        # remove /* ... */ comments
        while True:
            if text == str(re.sub('/\*(?:[^*]|\*(?!/))*\*/', '', text)):
                break
            text = re.sub('/\*(?:[^*]|\*(?!/))*\*/', '', text)
        # remove // comments
        while True:
            if text == str(re.sub('//[^\n]+', '', text)):
                break
            text = re.sub('//[^\n]+', '', text)
        return text
