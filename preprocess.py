import re
import unidecode
import contractions
import emoji


# remove accented characters
def remove_accented_chars(text):
    # unidecode() function of unidecode module takes a unicode string as input and
    # returns an ASCII string that approximates the original text, removing
    # accented characters from the text
    text = unidecode.unidecode(text)
    return text


# remove urls
def remove_url(text):
    return re.sub(r"http\S+", "", text).strip()


# remove symbols and digits
def remove_symbols_digits(text):
    return re.sub("[^a-zA-Z\s]", "", text)


# remove special characters
def remove_special_chars(text):
    # replace all instances of \r and \n with a single space
    text = re.sub(r"[\r\n]+", " ", text)
    # replace all instances of four or more spaces with a single space
    text = re.sub(r" {4,}", " ", text)
    # remove all double quotes
    text = re.sub(r'"', "", text)

    return text


# remove extra whitespace
def remove_extra_whitespace(text):
    # remove leading and trailing whitespace
    text = text.strip()
    # replace all sequences of whitespace with a single space
    text = re.sub(r"\s+", " ", text)

    return text


# fix word lengthening (characters are wrongly repeated)
def fix_repeated(text):
    # compile a regex pattern that matches any character that is repeated
    # two or more times consecutively
    pattern = re.compile(r"(.)\1{2,}")
    # replace all matches of the pattern with double instances of the same character
    return pattern.sub(r"\1\1", text)


def expand_abbreviations(text):
    abbreviations = {
        'afaik': 'as far as I know',
        'aka': 'also known as',
        'asl': 'age/sex/location',
        'b4': 'before',
        'bday': 'birthday',
        'btw': 'by the way',
        'cc': 'carbon copy',
        'cos': 'because',
        'ctn': 'cannot talk now',
        'cu': 'see you',
        'cuz': 'because',
        'diy': 'do it yourself',
        'dm': 'direct message',
        'fb': 'Facebook',
        'fomo': 'fear of missing out',
        'ftfy': 'fixed that for you',
        'fwiw': 'for what it\'s worth',
        'fyi': 'for your information',
        'gg': 'good game',
        'gj': 'good job',
        'gl': 'good luck',
        'gn': 'good night',
        'gr8': 'great',
        'gtfo': 'get the fuck out',
        'gtg': 'got to go',
        'hmu': 'hit me up',
        'icymi': 'in case you missed it',
        'idc': 'I don\'t care',
        'idk': 'I don\'t know',
        'ikr': 'I know, right?',
        'imo': 'in my opinion',
        'irl': 'in real life',
        'jk': 'just kidding',
        'lmao': 'laughing my ass off',
        'lmk': 'let me know',
        'lol': 'laugh out loud',
        'mfw': 'my face when',
        'nbd': 'no big deal',
        'nvm': 'never mind',
        'ofc': 'of course',
        'omg': 'oh my god',
        'ppl': 'people',
        'rofl': 'rolling on the floor laughing',
        'srsly': 'seriously',
        'tbh': 'to be honest',
        'tbt': 'throwback Thursday',
        'thx': 'thanks',
        'tl;dr': 'too long; didn\'t read',
        'tmi': 'too much information',
        'ttyl': 'talk to you later',
        'u': 'you',
        'wtf': 'what the fuck',
        'yolo': 'you only live once'
    }

    # create a regular expression pattern that matches any of the abbreviations in the `abbreviations` dictionary
    pattern = re.compile(r'\b(' + '|'.join(abbreviations.keys()) + r')\b')
    # apply the regular expression pattern to the input text and replace any matches with their corresponding expanded form
    expanded_text = pattern.sub(lambda x: abbreviations[x.group()], text)

    return expanded_text


def convert_emoji_to_text(text):
    return emoji.demojize(text, delimiters=("", ""))


def process_txt(text):
    text = convert_emoji_to_text(text)
    text = remove_accented_chars(text)
    text = expand_abbreviations(text)
    text = contractions.fix(text)
    text = text.lower()
    text = remove_url(text)
    text = remove_symbols_digits(text)
    text = remove_special_chars(text)
    text = remove_extra_whitespace(text)
    text = fix_repeated(text)

    return text

# print(process_txt("idk man wtf is wrong with you?"))
