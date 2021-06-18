import markovify as mf
import json
import argparse
import numpy as np

TEXT = "Ублюдок, мать твою, а ну иди сюда, говно собачье, решил ко мне лезть? Ты, засранец вонючий, мать твою, а? Ну иди сюда, попробуй меня трахнуть, я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят, иди идиот, трахать тебя и всю семью, говно собачье, жлоб вонючий, дерьмо, сука, падла, иди сюда, мерзавец, негодяй, гад, иди сюда, ты — говно, жопа!"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--source', type=str, required=True, help='link to a json file')
    p.add_argument('-f', '--first_words', type=str, default=None, help='a words to start a sentence')
    p.add_argument('-l', '--length', type=int, default=None, help='maximum length of sentence')
    p.add_argument('--state_size', type=int, default=2, help='Markov chain state size')
    return p.parse_args()


def apply_markov_chain(text, opt):
    model = mf.Text(text, state_size=opt.state_size)

    if opt.first_words:
        return model.make_sentence_with_start(opt.first_words, strict=False)
    elif opt.length:
        return model.make_short_sentence(max_chars=opt.length)
    else:
        return model.make_sentence()


def main(opt):
    with open(opt.source, 'r') as f:
        text_json = json.load(f)

    # text = TEXT
    text_list = []
    for item in text_json['items']:
        text_list.append((item['text']).replace('<p>', ' ').replace('</p>', ''))

    text = ''.join(text_list)

    res = apply_markov_chain(text.lower(), opt)
    print(res)


if __name__ == '__main__':
    main(parse_args())
