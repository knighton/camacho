# -*- encoding: utf-8 -*-

from camacho.base import TransformerMixin
from camacho.preprocess.tokenize import CharacterTokenizer
from camacho.preprocess.sequences import SequenceDestutterer
import sys
import unicodedata


class WhitespaceNormalizer(TransformerMixin):
    """
    Replace all whitespace with ' '.
    """

    def transform(self, texts):
        return map(lambda s: u' '.join(s.split()), texts)


class EllipsisNormalizer(TransformerMixin):
    """
    Normalize various strings of dots to a dot or an ellipsis.
    """

    def __init__(self):
        self._ellipsis = unichr(0x2026)

    def _transform_text(self, text):
        text = text.replace(self._ellipsis, '...')
        inside_dots = False
        num_dots = None
        for i, c in enumerate(text):
            if inside_dots:
                if c == '.':
                    num_dots += 1
                elif not c.isspace():
                    if num_dots == 1:
                        c = '.'
                    else:
                        c = self._ellipsis
                    rr.append(c)
                    inside_dots = False
            else:
                if c == '.':
                    inside_dots = True
                    num_dots = 1
                else:
                    rr.append(c)
        return ''.join(rr)

    def transform(self, texts):
        return map(self._transform_text, texts)


class TextDestutterer(TransformerMixin):
    """
    Drop overly-repeated non-digit characters.
    """

    def __init__(self, max_consec=3):
        ignore = []
        for c in map(unichr, xrange(sys.maxunicode)):
            cat = unicodedata.category(c)
            if cat.startswith('N'):
                ignore.append(c)
        self._des = SequenceDestutterer(max_consec=max_consec, ignore=ignore)
        self._tok = CharacterTokenizer()

    def transform(self, texts):
        ccc = self._tok.transform(texts)
        ccc = self._des.transform(ccc)
        return map(lambda cc: ''.join(cc), ccc)


class CharacterReplacer(TransformerMixin):
    """
    Replace characters (single code units) with strings.
    """

    def __init__(self, s2s=None):
        if s2s is None:
            s2s = {}
        self._s2s = s2s
        for k, v in self._s2s.iteritems():
            assert isinstance(k, (str, unicode))
            assert len(k) == 1
            assert isinstance(v, (str, unicode))

    def transform(self, texts):
        rr = []
        for text in texts:
            cc = list(text)
            for i, c in enumerate(cc):
                v = self._s2s.get(c, None)
                if v is not None:
                    cc[i] = v
            rr.append(''.join(cc))
        return rr


# Latin Letter Small Capital (note that there is no Q and X)
# source: http://en.wikipedia.org/wiki/Small_caps#Unicode
SMALL_CAPS = {
    u"\u1d00": 'A', u"\u0299": 'B', u"\u1d04": 'C', u"\u1d05": 'D',
    u"\u1d07": 'E', u"\ua730": 'F', u"\u0262": 'G', u"\u029C": 'H',
    u"\u026A": 'I', u"\u1d0a": 'J', u"\u1d0b": 'K', u"\u029f": 'L',
    u"\u1d0d": 'M', u"\u0274": 'N', u"\u1d0f": 'O', u"\u1d18": 'P',
    u"\u0280": 'R', u"\ua731": 'S', u"\u1d1b": 'T', u"\u1d1c": 'U',
    u"\u1d20": 'V', u"\u1d21": 'W', u"\u028f": 'Y', u"\u1d22": 'Z',
}


MISC_LATIN = {
    # latin small letter script
    u"\u0261": 'g',
    # double-struck capitals
    u"\u2102": 'C', u"\u210d": 'H', u"\u2115": 'N', u"\u2119": 'P',
    u"\u211a": 'Q', u"\u211d": 'R', u"\u2124": 'Z',
    # double-struck italic capitals
    u"\u2145": 'D',
    # double-struck italic small
    u"\u2146": 'd', u"\u2147": 'e', u"\u2148": 'i', u"\u2149": 'j',
    # script capital
    u"\u210b": 'H', u"\u2110": 'I', u"\u2112": 'L', u"\u2133": 'M',
    u"\u2118": 'P', u"\u211b": 'R', u"\u212c": 'B',
    u"\u2130": 'E', u"\u2131": 'F',
    # script small
    u"\u210a": 'g', u"\u2113": 'l', u"\u212f": 'e', u"\u2134": 'o',
}


MISC_NONLETTER = {
    u'\xa0': ' ',  # map non-breaking space to regular space
}


def map_range(dest_first, source_first, length):
    """
    :param dest_first: index of the beginning of the destination range
    :param source_fist: index of the beginning of the source range
    :param length: length of the the range to be mapped
    """
    offset = source_first - dest_first
    for k in xrange(source_first, source_first + length):
        yield k, k - offset


# map zero-width characters to nothing
# (also see https://stackoverflow.com/questions/8733233/)
ZERO_WIDTH_MAP = dict.fromkeys(
    range(ord(u'\x00'), ord(u'\x08') + 1) +
    range(ord(u'\x0b'), ord(u'\x0c') + 1) +
    range(ord(u'\x0e'), ord(u'\x1f') + 1) +
    range(ord(u'\x7f'), ord(u'\x9f') + 1) +
    [ord(u'\xad')] +
    range(ord(u'\u17b4'), ord(u'\u17b5') + 1) +
    range(ord(u'\u200b'), ord(u'\u200f') + 1) +
    range(ord(u'\u202a'), ord(u'\u202d') + 1) +
    range(ord(u'\u2060'), ord(u'\u2064') + 1) +
    range(ord(u'\u206a'), ord(u'\u206f') + 1) +
    [ord(u'\ufeff')] +
    [ord(u'\uffff')]
)


# note: directional characters not really properly handled (we remove them)
DIRECTIONAL_MAP = dict.fromkeys(
    # treat directional overrides as zero-width
    # http://ilug.linux.ie.narkive.com/5nWeU5DX/ot-a-spammer-who-knows-unicode
    # e.g. D%u202Erae%u202C Bar%u202Eyalc%u202Cs M%u202Ebme%u202Cer,
    # reads as "Dear Barclays Member,"
    # as you can see by rendering it at
    # http://unicode.online-toolz.com/tools/text-unicode-entities-convertor.php
    [ord(u'\u202a'), ord(u'\u202b')] +
    [ord(u'\u202d'), ord(u'\u202e'), ord(u'\u202c')] +
    [ord(u'\u200e'), ord(u'\u200f')]
)


# variation selectors are used to specify how emoji character
# should be displayed for example. Ignore them because they
# carry little semantic meaning and are noisy.
VARIATION_SELECTORS_MAP = dict.fromkeys(
    range(ord(u'\ufe00'), ord(u'\ufe0f') + 1)
)


# handled by NFKC (so it is redundant to add these)
FULL_WIDTH_MAP = dict(map_range(33, 65281, 94))
CIRCLED_CAPS_MAP = dict(map_range(65, 9398, 26))
CIRCLED_SMALL_MAP = dict(map_range(97, 9424, 26))


# partially handled by NFKC
MISC_LATIN_MAP = {ord(k): ord(v) for k, v in MISC_LATIN.iteritems()}


SMALL_CAPS_MAP = {ord(k): ord(v) for k, v in SMALL_CAPS.iteritems()}
MISC_NONLETTER_MAP = {ord(k): ord(v) for k, v in MISC_NONLETTER.iteritems()}
COMBINING_MAP = dict.fromkeys(
    c for c in xrange(sys.maxunicode) if unicodedata.combining(unichr(c)))


# handled by NFKC if you have a wide Python build
HIGH_SURROGATE_MAP = dict.fromkeys(xrange(ord(u'\ud800'), ord(u'\udbff') + 1))
VANILLA = u"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BLACKLETTER = u"𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"
BLACKLETTER_BOLD = u"𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
BLACKLETTER_MAP = {ord(k): ord(v) for k, v in chain(
    izip(BLACKLETTER.translate(HIGH_SURROGATE_MAP), VANILLA),
    izip(BLACKLETTER_BOLD.translate(HIGH_SURROGATE_MAP), VANILLA)
)}


def sum_dicts(*args):
    """
    Return a sum total of several dictionaries.

    Note: this is non-commutative (later entries override earlier).
    """
    result = dict()
    for arg in args:
        result.update(arg)
    return result


DEFAULT_TRANSLATE_MAP = sum_dicts(
    ZERO_WIDTH_MAP, VARIATION_SELECTORS_MAP,

    # Handled by NFKC.
    FULL_WIDTH_MAP, CIRCLED_CAPS_MAP, CIRCLED_SMALL_MAP,

    # Partially handled by NFKC.
    MISC_LATIN_MAP,

    SMALL_CAPS_MAP, MISC_NONLETTER_MAP
)


EXTRA_TRANSLATE_MAP = sum_dicts(
    DEFAULT_TRANSLATE_MAP, HIGH_SURROGATE_MAP, BLACKLETTER_MAP)


class ExtraNFK(TransformerMixin):
    """
    Apply further Unicode compatibility mappings than the NFK* forms.
    """

    def __init__(self):
        self._replacer = CharacterReplacer(EXTRA_TRANSLATE_MAP)

    def fit(self, texts):
        self._replacer.fit(texts)
        return self

    def transform(self, texts):
        return self._replacer.transform(texts)
