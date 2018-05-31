import apertium
from apertium.utils import to_alpha3_code, execute
from utils import init_paths, init_pairs_graph, get_pipeline



def get_pair_or_error(langpair, text_length):
    try:
        l1, l2 = map(to_alpha3_code, langpair.split('|'))
    except ValueError:
        print("Pair is Invalid")
        return None
    if '%s-%s' % (l1, l2) not in apertium.pairs:
        print("Pair is not Installed")
        return None
    else:
        return (l1, l2)


def get_format(format, deformat, reformat):
    if format:
        deformat = 'apertium-des' + format
        reformat = 'apertium-re' + format
    else:
        if 'apertium-des' not in deformat:
            deformat = 'apertium-des' + deformat
        if 'apertium-re' not in reformat:
            reformat = 'apertium-re' + reformat

    return deformat, reformat


def translate_and_respond(self, pair, pipeline, to_translate, mark_unknown, nosplit=False, deformat=True, reformat=True):
        mark_unknown = mark_unknown in ['yes', 'true', '1']
        translated = translate(to_translate, nosplit, deformat, reformat)
        val = maybe_strip_marks(mark_unknown, pair, translated)
        return val

def transalate(langpair, text, markUnknown='yes', format=None, deformat='html', reformat='html-noent'):
	init_pairs_graph()
	init_paths()
    pair = get_pair_or_error(langpair), len(text)
    if pair is not None:
        pipeline = get_pipeline(pair)
        deformat, reformat = get_format(format, deformat, reformat)
        return translate_and_respond(pair,
                                         pipeline,
                                         text,
                                         markUnknown,
                                         nosplit=False,
                                         deformat=deformat,
                                         reformat=reformat)