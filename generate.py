import argparse
import markovify as mf

import json
import string

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--first_words', type=str, default=None, help='a words to start a sentence')
    p.add_argument('-l', '--length', type=int, default=None, help='maximum length of sentence')
    p.add_argument('-s', '--state_size', type=int, default=2, help='Markov chain state size')
    p.add_argument('-p', '--add_punctuation', action='store_false', help="if present, the punctuation won't be deleted")
    return p.parse_args()


def apply_markov_chain(model, opt):
    # model = mf.Text(text, state_size=opt.state_size)

    if opt.first_words:
        return model.make_sentence_with_start(opt.first_words, strict=False)
    elif opt.length:
        return model.make_short_sentence(max_chars=opt.length)
    else:
        return model.make_sentence()


def main(opt):
    with open("/home/vyacheslav/Projects/congrats/scraped/greetings-data.json", 'r') as f:
        text_json_putin = json.load(f)

    with open("/home/vyacheslav/Projects/congrats/scraped/congratulations.json", 'r') as f:
        text_json_general = json.load(f)

    text_list_general = []
    for item in text_json_general['items']:
        text_list_general.append((item['text']).replace('<p>', ' ').replace('</p>', ''))

    text_general = ''.join(text_list_general).lower()


    text_list_putin = []
    for item in text_json_putin['items']:
        text_list_putin.append((item['text']).replace('<p>', ' ').replace('</p>', ''))

    text_putin = ''.join(text_list_putin).lower()

    if opt.add_punctuation:
        text_general = text_general.translate(str.maketrans('', '', string.punctuation))  # remove punctuation instead of re
        text_putin = text_putin.translate(str.maketrans('', '', string.punctuation))

    model = mf.combine(
        [mf.Text(text_general, state_size=opt.state_size), mf.Text(text_putin, state_size=opt.state_size)],
        [1, 0.3]
    )

    res = apply_markov_chain(model, opt)

    print(res)


if __name__ == '__main__':
    main(parse_args())
