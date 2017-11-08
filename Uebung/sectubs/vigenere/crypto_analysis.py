eng_freq=[8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8, 4.0, 2.4,
          6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]
eng_comb=['th', 'ea', 'of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if',
          'me', 'my', 'up', 'the', 'est', 'for', 'and', 'ent', 'his', 'tha']
ger_freq=[6.51, 1.89, 3.06, 5.08, 17.4, 1.66, 3.01, 4.76, 7.55, 0.27, 1.21, 3.44, 2.53,
          9.78, 2.51, 0.79, 0.02, 7.0, 7.27, 6.15, 4.35, 0.67, 1.89, 0.03, 0.04, 1.13]
ger_comb=['er', 'en', 'ch', 'de', 'ei', 'nd', 'ie', 'te', 'in', 'ein', 'ich', 'nde', 'die',
          'und', 'che', 'end', 'gen', 'sch', 'cht', 'den']

freq = {"eng": eng_freq, "ger": ger_freq}
comb = {"eng": eng_comb, "ger": ger_comb}

"""
    The maximal score - and also the base score - for a given frequency set. Works only for small alphabet.
    :param freq_list: The used frequency list for the small alphabet
    :return: The max score as number
"""
def max_score(freq_list):
    score = 0;
    for freq in freq_list:
        score += 100*freq
    return score


"""
    Analyses a given message for the possibility to be a real text in the given language (default = eng).
    A higher score means the message is more likely to be a real text.
    Language codes: English="eng", German = "ger"
    :param lang: The language for the analysis
    :param message: The message to analyse
    :return: The analysis score, higher means better
"""
def analysis(message: str, lang = "eng"):
    base_score = max_score(freq[lang])
    for i in range(0, 25):
        count = message.count(chr(i+97))
        should = eng_freq[i]
        base_score -= abs(should - count) * should

    actual_comb = comb[lang]
    for i in range(0, len(actual_comb) - 1):
        letter_comb = actual_comb[i]
        comb_score = 1
        for c in letter_comb:
            comb_score *= eng_freq[ord(c) - 97] / 100
        comb_score = 100*(1-comb_score)
        base_score += message.count(letter_comb) * comb_score

    return base_score
