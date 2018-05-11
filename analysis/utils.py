from iso639 import iso639Codes


def to_alpha3_code(code):

    iso639_codes_inverse = {v: k for k, v in iso639Codes.items()}

    if '_' in code:
        code, variant = code.split('_')
        return '%s_%s' % ((iso639_codes_inverse[code],
                           variant) if code in iso639_codes_inverse else (
            code,
            variant))
    else:
        return iso639_codes_inverse[code] if code in iso639_codes_inverse else code


def remove_dot_from_deformat(query, analyses):
    """
    When using the txt format, a dot is added at EOF (also, double line
    breaks) if the last part of the query isn't itself a dot
    """
    if not query[-1] == '.':
        return analyses[:-1]
    else:
        return analyses
