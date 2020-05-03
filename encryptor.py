import argparse
import string
import codecs
import sys
from collections import defaultdict
import pickle


def alphabetlanguage(language):
    global alphabet
    alphabet = ''
    if language == "rus":
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    elif language == "eng":
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
    elif language == "vern":
        for i in range(16):
            alphabet += chr(ord('a') + i)
    else:
        print("wrong language")
        sys.exit(0)
    alphabet += alphabet.upper()
    alphabet += string.punctuation
    alphabet += ' '


class Caesar:

    def encode(self, txt, key):
        output = ''
        if key < 0:
            key = len(alphabet) + key
        for i in txt:
            if i in alphabet:
                n = (alphabet.find(i) + key) % len(alphabet)
                output += alphabet[n]
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
            if i in alphabet:
                n = alphabet.find(i) + (alphabet.find(key[counter % len(key)]))
                n %= len(alphabet)
                output += alphabet[n]
                counter += 1
            else:
                output += i
        return output

    def decode(self, txt, key):
        key1 = ''
        for i in range(len(key)):
            n = len(alphabet) - alphabet.find(key[i])
            n %= len(alphabet)
            key1 += alphabet[n]
        return self.encode(txt, key)


def train(txt):
    k = 0
    d = defaultdict(int)
    for i in txt:
        if i in alphabet:
            try:
                d[i] += 1
            except KeyError:
                d[i] = 1
            k += 1
    for i in alphabet:
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
    minsum = 100 * len(alphabet)
    sum = 0
    minkey = 0
    for key in range(len(alphabet)):
        for i in range(len(alphabet)):
            n = txtanalysis[alphabet[(i + key) % len(alphabet)]]
            n -= model[alphabet[i]]
            sum += n ** 2
        if minsum > sum:
            minsum = sum
            minkey = key
        sum = 0
    obj = Caesar()
    return (obj.decode(txt, minkey))


class Vernam:

    def encode(self, txt, key):
        output = ''
        counter = 0
        for i in txt:
            if i in alphabet:
                n = alphabet.find(key[counter]) ^ alphabet.find(i)
                n %= len(alphabet)
                output += alphabet[n]
                counter += 1
            elif i.lower() in alphabet:
                n = alphabet.find(key[counter]) ^ alphabet.find(i.lower())
                n %= len(alphabet)
                output += (alphabet[n]).upper()
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


def TryInputFile(inputfile):
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


def TryOutputfile(outputfile, inputtxt):
    if outputfile:
        try:
            output_file(outputfile, inputtxt)
        except PermissionError:
            print("File access denied")
            sys.exit(0)
    else:
        print(inputtxt)


def TryCaesarKey(key):
    try:
        return int(key)
    except ValueError:
        print("Key must be integer")
        sys.exit(0)


def TryVigenereKey(key):
    for i in key:
        if i not in alphabet:
            print("Key symbols must be in alphabet")
            sys.exit(0)


def TryVernamKey(key, txt, nomod):
    if len(key) != len(txt):
        print("Key must be same lenght with text")
        sys.exit(0)
    if nomod:
        if len(alphabet) != 16:
            print("Wrong alphabet for vernam")
            sys.exit(0)
        TryVigenereKey(key)


def Encode(cipher, key, inputfile, outputfile, language):
    alphabetlanguage(language)
    txt = TryInputFile(inputfile)
    if cipher == 'caesar':
        key = TryCaesarKey(key)
        caes = Caesar()
        inputtxt = caes.encode(txt, key)
    elif cipher in ('vigenere', 'vernammod'):
        TryVigenereKey(key)
        if cipher == 'vernammod':
            TryVernamKey(key, txt, False)
        vig = Vigenere()
        inputtxt = vig.encode(txt, key)
    elif cipher == 'vernam':
        TryVernamKey(key, txt, True)
        ver = Vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return
    TryOutputfile(outputfile, inputtxt)


def Decode(cipher, key, inputfile, outputfile, language):
    alphabetlanguage(language)
    txt = TryInputFile(inputfile)
    if cipher == 'caesar':
        key = TryCaesarKey(key)
        caes = Caesar()
        inputtxt = caes.decode(txt, int(key))
    elif cipher in ('vigenere', 'vernammod'):
        TryVigenereKey(key)
        if cipher == 'vernammod':
            TryVernamKey(key, txt, False)
        vig = Vigenere()
        inputtxt = vig.decode(txt, key)
    elif cipher == 'vernam':
        TryVernamKey(key, txt, True)
        ver = Vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return
    TryOutputfile(outputfile, inputtxt)


def Train(text, model, language):
    alphabetlanguage(language)
    txt = TryInputFile(text)
    try:
        with open(model, 'wb') as f:
            pickle.dump(train(txt), f)
    except PermissionError:
        print("Not way to output model file")
        return


def Hack(inputfile, outputfile, modelfile, language):
    alphabetlanguage(language)
    try:
        with open(modelfile, 'rb') as f:
            model = pickle.load(f)
    except Exception:
        print("I can't read model file")
        return
    txt = TryInputFile(inputfile)
    try:
        outputtxt = hack(txt, model)
    except Exception:
        print("Problem with model")
        return
    TryOutputfile(outputfile, outputtxt)


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

    if args.work == 'encode':
        Encode(args.cipher, args.key, args.input, args.output, args.language)
    elif args.work == 'decode':
        Decode(args.cipher, args.key, args.input, args.output, args.language)
    elif args.work == 'train':
        Train(args.text, args.model, args.language)
    elif args.work == 'hack':
        Hack(args.input, args.output, args.model, args.language)


if __name__ == '__main__':
    main()
