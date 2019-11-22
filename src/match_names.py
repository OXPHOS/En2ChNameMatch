import argparse
import os
import pickle
from src import dict_path
from src import generate_trie, utils


def load_trie(f):
    with open(f, 'rb') as file:
        trie = pickle.load(file, encoding='UTF-8')
    return trie


def single_word_lookup(k, output_to_screen=True):
    k = k.lower()
    if trie.has_key(k):
        res = trie[k]['Region:CH']
        if output_to_screen:
            utils.prYellow(res)
        return res
    else:
        if output_to_screen:
            utils.prRed("Word not found.")
        return ''


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=None,
                        help='Path to the input file. Entries separated by comma or return')
    parser.add_argument('--kind', type=str, default='Both',
                        help='Translate Name, Place and Both')
    args, unparsed = parser.parse_known_args()

    if args.kind == 'Name' or args.kind == 'name':
        f = os.path.join(dict_path, '人名词典')
        if os.path.isfile(f):
            trie = load_trie(f)
        else:
            trie = generate_trie.generate_person_trie(f)
        print('Matching person name only. Total entries: %i' % len(trie))
    elif args.kind == 'Place' or args.kind == 'place':
        f = os.path.join(dict_path, '地名词典')
        if os.path.isfile(f):
            trie = load_trie(f)
        else:
            trie = generate_trie.generate_place_trie(f)
        print('Matching place name only. Total entries: %i' % len(trie))
    else:
        f = os.path.join(dict_path, '人名+地名词典')
        if os.path.isfile(f):
            trie = load_trie(f)
        else:
            trie = generate_trie.generate_merge_trie(f)
        print('Matching both person and place names. Total entries: %i' % len(trie))


    if args.file and os.path.isfile(args.file):
        print("Activating file mode...")
        output = []
        with open(args.file, encoding='utf-8') as fp:
            for line in fp.readlines():
                line = line.strip('\n')

                if not line:
                    break

                for word in line.split(','):
                    word = word.strip()
                    if ' ' in word:
                        res = single_word_lookup(word, output_to_screen=False)
                        if res:
                            output.append(word+': '+res)
                        else:
                            for w in word.split():
                                output.append(w+': '+single_word_lookup(w, output_to_screen=False))
                    else:
                        output.append(word + ': ' + single_word_lookup(word, output_to_screen=False))

        with open('output.txt', 'w') as fp:
            fp.writelines("%s\n" %_ for _ in output)
        print("Done.")

    else:
        print("Activating interactive mode...")
        key = input("Enter a name to be translated (Enter 'exit' to exit) >> ")
        while key != 'exit':
            key = key.strip()
            if ' ' in key:
                res = single_word_lookup(key)
                if not res:
                    for w in key.split():
                        utils.prYellow('>>>' + w)
                        single_word_lookup(w)
            else:
                single_word_lookup(key)
            key = input("Enter a name to be translated. Enter 'exit' to end. >> ")
