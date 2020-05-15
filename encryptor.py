import argparse
import string
import codecs
import sys
from collections import defaultdict
import pickle


def alphabetlanguage(language):
    global ALPHABET
    ALPHABET = ''
    if language == "rus":
        ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    elif language == "eng":
        ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    elif language == "vern":
        for i in range(16):
            ALPHABET += chr(ord('a') + i)
    else:
        print("wrong language")
        sys.exit(0)
    ALPHABET += ALPHABET.upper()
    ALPHABET += string.punctuation
    ALPHABET += ' '


class Caesar:

    def encode(self, txt, key):
        output = ''
        for i in txt:
            if i in ALPHABET:
                n = (ALPHABET.find(i) + key) % len(ALPHABET)
                output += ALPHABET[n]
            else:
                output += i
        return output

    def decode(self, txt, key):
        key *= -1
        return self.encode(txt, key)


class Vigenere:

    def encode(self, txt, key):
        counter = 0
        output = ''
        for i in txt:
            if i in ALPHABET:
                n = ALPHABET.find(i) + (ALPHABET.find(key[counter % len(key)]))
                n %= len(ALPHABET)
                output += ALPHABET[n]
                counter += 1
            else:
                output += i
        return output

    def decode(self, txt, key):
        key1 = ''
        for i in range(len(key)):
            n = len(ALPHABET) - ALPHABET.find(key[i])
            n %= len(ALPHABET)
            key1 += ALPHABET[n]
        return self.encode(txt, key)


def train(txt):
    k = 0
    d = defaultdict(int)
    for i in txt:
        if i in ALPHABET:
            d[i] += 1
            k += 1
    for i in ALPHABET:
        if i not in d:
            d[i] = 0
    try:
        for j in d:
            d[j] *= 100 / k
    except ZeroDivisionError:
        print("Model file is empty")
        sys.exit(0)
    return d


def hack(txt, model):
    txtanalysis = train(txt)
    minsum = 100 * len(ALPHABET)
    sum = 0
    minkey = 0
    for key in range(len(ALPHABET)):
        for i in range(len(ALPHABET)):
            n = txtanalysis[ALPHABET[(i + key) % len(ALPHABET)]]
            n -= model[ALPHABET[i]]
            sum += n ** 2
        if minsum > sum:
            minsum = sum
            minkey = key
        sum = 0
    obj = Caesar()
    return obj.decode(txt, minkey)


class Vernam:

    def encode(self, txt, key):
        output = ''
        counter = 0
        for i in txt:
            if i in ALPHABET:
                n = ALPHABET.find(key[counter]) ^ ALPHABET.find(i)
                n %= len(ALPHABET)
                output += ALPHABET[n]
                counter += 1
            elif i.lower() in ALPHABET:
                n = ALPHABET.find(key[counter]) ^ ALPHABET.find(i.lower())
                n %= len(ALPHABET)
                output += (ALPHABET[n]).upper()
                counter += 1
            else:
                output += i
        return output

    def decode(self, txt, key):
        return self.encode(txt, key)


def input_file(file):
    try:
        with codecs.open(file, "r", "utf-8") as text:
            txt = text.read()
    except UnicodeDecodeError:
        with open(file, "r") as text:
            txt = text.read()
    return txt


def output_file(file, output_txt):
    with open(file, "w") as text:
        text.write(output_txt)


def try_input_file(inputfile):
    txt = ''
    if inputfile:
        try:
            txt = input_file(inputfile)
        except FileNotFoundError:
            print("File not found")
            sys.exit(0)
    else:
        txt = input()
    return txt


def try_output_file(outputfile, inputtxt):
    if outputfile:
        try:
            output_file(outputfile, inputtxt)
        except PermissionError:
            print("File access denied")
            sys.exit(0)
    else:
        print(inputtxt)


def try_caesar_key(key):
    try:
        return int(key)
    except ValueError:
        print("Key must be integer")
        sys.exit(0)


def try_vigenere_key(key):
    for i in key:
        if i not in ALPHABET:
            print("Key symbols must be in ALPHABET")
            sys.exit(0)


def try_vernam_key(key, txt, nomod):
    if len(key) != len(txt):
        print("Key must be same lenght with text")
        sys.exit(0)
    if nomod:
        if len(ALPHABET) != 16:
            print("Wrong alphabet for vernam")
            sys.exit(0)
        try_vigenere_key(key)


def encode_call(cipher, key, inputfile, outputfile):
    txt = try_input_file(inputfile)
    if cipher == 'caesar':
        key = try_caesar_key(key)
        caes = Caesar()
        inputtxt = caes.encode(txt, key)
    elif cipher in ('vigenere', 'vernammod'):
        try_vigenere_key(key)
        if cipher == 'vernammod':
            try_vernam_key(key, txt, False)
        vig = Vigenere()
        inputtxt = vig.encode(txt, key)
    elif cipher == 'vernam':
        try_vernam_key(key, txt, True)
        ver = Vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return
    try_output_file(outputfile, inputtxt)


def decode_call(cipher, key, inputfile, outputfile):
    txt = try_input_file(inputfile)
    if cipher == 'caesar':
        key = try_caesar_key(key)
        caes = Caesar()
        inputtxt = caes.decode(txt, int(key))
    elif cipher in ('vigenere', 'vernammod'):
        try_vigenere_key(key)
        if cipher == 'vernammod':
            try_vernam_key(key, txt, False)
        vig = Vigenere()
        inputtxt = vig.decode(txt, key)
    elif cipher == 'vernam':
        try_vernam_key(key, txt, True)
        ver = Vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return
    try_output_file(outputfile, inputtxt)


def train_call(text, model):
    txt = try_input_file(text)
    try:
        with open(model, 'wb') as f:
            pickle.dump(train(txt), f)
    except PermissionError:
        print("Not way to output model file")
        return


def hack_call(inputfile, outputfile, modelfile):
    try:
        with open(modelfile, 'rb') as f:
            model = pickle.load(f)
    except Exception:
        print("I can't read model file")
        return
    txt = try_input_file(inputfile)
    try:
        outputtxt = hack(txt, model)
    except Exception:
        print("Problem with model")
        return
    try_output_file(outputfile, outputtxt)


def arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='work', help='What program do')

    encode = subparsers.add_parser('encode', help='encode')  # encode
    encode.add_argument('--cipher', help='cipher - caesar/'
                                         'vigenere/'
                                         'vernammod/'
                                         'vernam')
    encode.add_argument('--key', dest='key', help='key'
                                                  '/integer for caesar'
                                                  '/string lowercase letters'
                                                  ' for vigenere'
                                                  '/file lenght string '
                                                  'lowercase letters '
                                                  'for vernammod'
                                                  '/file lenght string '
                                                  'with first 16 lowercase'
                                                  ' letters for vernam')
    encode.add_argument('--input-file', dest='input', help='path '
                                                           'to input file')
    encode.add_argument('--output-file', dest='output', help='path '
                                                             'to output file')
    encode.add_argument('--language', dest='language', help='rus if cirillic/'
                                                            'eng if latin/'
                                                            'vern if vernam'
                                                            'cipher')

    decode = subparsers.add_parser('decode', help='decode')  # decode
    decode.add_argument('--cipher', help='cipher - caesar/'
                                         'vigenere/'
                                         'vernammod/'
                                         'vernam')
    decode.add_argument('--key', dest='key', help='key'
                                                  '/integer for caesar'
                                                  '/string lowercase letters'
                                                  ' for vigenere'
                                                  '/file lenght string '
                                                  'lowercase letters '
                                                  'for vernammod'
                                                  '/file lenght string'
                                                  ' with first 16 lowercase '
                                                  'letters for vernam')
    decode.add_argument('--input-file', dest='input', help='path to '
                                                           'input file')
    decode.add_argument('--output-file', dest='output', help='path to '
                                                             'output file')
    decode.add_argument('--language', dest='language', help='rus if cirillic/'
                                                            'eng if latin'
                                                            'vern if vernam'
                                                            'cipher')

    train = subparsers.add_parser('train', help='train')  # train
    train.add_argument('--text-file', dest='text', help='path '
                                                        'to input text file')
    train.add_argument('--model-file', dest='model', help='output model file')
    train.add_argument('--language', dest='language', help='rus if cirillic/'
                                                           'eng if latin')

    hack = subparsers.add_parser('hack', help='hack')  # hack
    hack.add_argument('--input-file', dest='input', help='path to input file')
    hack.add_argument('--output-file', dest='output', help='path to '
                                                           'output file')
    hack.add_argument('--model-file', dest='model', help='input model file')
    hack.add_argument('--language', dest='language', help='rus if cirillic/'
                                                          'eng if latin')

    args = parser.parse_args()
    return args


def main():

    args = arguments()

    alphabetlanguage(args.language)

    if args.work == 'encode':
        encode_call(args.cipher, args.key, args.input,
                    args.output)
    elif args.work == 'decode':
        decode_call(args.cipher, args.key, args.input,
                    args.output)
    elif args.work == 'train':
        train_call(args.text, args.model)
    elif args.work == 'hack':
        hack_call(args.input, args.output, args.model)


if __name__ == '__main__':
    main()

