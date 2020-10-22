import os
from pymorphy2.tokenizers import simple_word_tokenize
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import pandas as pd
import re
from itertools import product

from flask import Flask, request, render_template, send_file
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

names = []
sents = []
lemma_seq = []
pos_seq = []

directory = 'C:\\Users\\Yana\\Desktop\\project\\corpus'
walk = [(x, y, z) for x, y, z in os.walk(directory)]

corpus = pd.read_csv('corpus.csv', index_col=0)
main_dict = dict(corpus)

def combine_sent(sent, lemma_seq, pos_seq):
    tokens = simple_word_tokenize(sent)
    norm_tokens = [token for token in tokens if token[0].isalpha()]
    if type(lemma_seq) != str:
        return []
    lemmas = lemma_seq.split()
    pos = pos_seq.split()
    combined_list = []
    for i in range(len(pos)):
        combined_list.append(' ' + norm_tokens[i] + '|' + lemmas[i] + '|' + pos[i])
    return combined_list

def make_combos(words):
    word_combos = []
    if len(words) == 3:
        combos = list(product(words[0], words[1], words[2]))
        for c in combos:
            word_combos.append('.'.join(c))
    elif len(words) == 2:
        combos = list(product(words[0], words[1]))
        for c in combos:
            word_combos.append('.'.join(c))
    else:
        word_combos = words[0]
    return word_combos

def search_func(main_dict, ans_dict, s_words):
    lemmas = main_dict['lemmas']
    for j in range(len(lemmas)):
        c_list = combine_sent(main_dict['sents'][j], main_dict['lemmas'][j], main_dict['pos'][j])
        for i in range(len(c_list)-len(s_words)+1):
            if s_words[0] in c_list[i]:
                if len(s_words) > 1 and s_words[1] in c_list[i+1]:
                    if len(s_words) == 3 and s_words[2] in c_list[i+2]:
                        ans_dict['sents'].append(main_dict['sents'][j])
                        ans_dict['source'].append(main_dict['source'][j])
                        key_words = [c.split('|')[0] for c in c_list[i:i+3]]
                        ans_dict['key_words'].append(' '.join(key_words))
                    elif len(s_words) == 2:
                        ans_dict['sents'].append(main_dict['sents'][j])
                        ans_dict['source'].append(main_dict['source'][j])
                        key_words = [c.split('|')[0] for c in c_list[i:i+2]]
                        ans_dict['key_words'].append(' '.join(key_words))
                elif len(s_words) == 1:
                    ans_dict['sents'].append(main_dict['sents'][j])
                    ans_dict['source'].append(main_dict['source'][j])
                    key_words = c_list[i].split('|')[0]
                    ans_dict['key_words'].append(key_words)
    return ans_dict

def mixed_search_upd(seq, main_dict):
    ans_dict = {'source': [], 'sents': [], 'key_words': []}

    s_words = seq.split(' ')
    for i in range(len(s_words)):
        if '"' in s_words[i]:
            s_words[i] = [' ' + s_words[i].replace('"', '') + '|']
        elif '+' in s_words[i]:
            parts = s_words[i].split('+')
            s_words[i] = [parts[0] + '|' + parts[1]]
        elif not s_words[i].isupper():
            normal_forms = []
            for m in morph.parse(s_words[i]):
                if m.normal_form not in normal_forms:
                    normal_forms.append(m.normal_form)
            if len(normal_forms) < 2:
                s_words[i] = ['|' + s_words[i].lower() + '|']
            else:
                s_words[i] = ['|' + word + '|' for word in normal_forms]
        else:
            s_words[i] = [s_words[i]]
    combos = make_combos(s_words)

    ans = []
    for combo in combos:
        ans_dict = search_func(main_dict, ans_dict, combo.split('.'))
    return ans_dict


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    ans_dict = mixed_search_upd(text, main_dict)
    ans_list = []
    no_tag_list = []
    sources = ans_dict['source']
    texts = ans_dict['sents']
    keys = ans_dict['key_words']
    for i in range(len(texts)):
        if len(ans_list) <= 20:
            key_reg = '\W+'.join(keys[i].split())
            new_s = re.sub(r'(\W|^)({})(\W|$)'.format(key_reg), r'\1<b>\2</b>\3', texts[i])
            ans_list.append(new_s + ' | <i>' + sources[i] + '</i>')
        no_tag_list.append(texts[i] + ' ИСТОЧНИК: ' + sources[i])
    with open('templates\\all_answers.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(no_tag_list))
    page_ans = '<br><br>'.join(ans_list)
    with open('templates\\answers.html', 'w', encoding='utf-8') as f:
        f.write(page_ans)
    return render_template('answer.html', variable=len(no_tag_list))

@app.route('/download_file.html')
def download():
    # return render_template('templates\\all_answers.txt')
    return send_file('templates\\all_answers.txt', as_attachment=True, cache_timeout=0)

if __name__ == '__main__':
    app.run()
