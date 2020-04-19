import argparse
import string
import codecs

alphabet0 = 'abcdefghijklmnopqrstuvwxyz'
alphabet0 += alphabet0.upper()
alphabet0 += string.punctuation
alphabet0 += ' '

alphabet1 = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alphabet1 += alphabet1.upper()
alphabet1 += string.punctuation
alphabet1 += ' '

alphabet2 = ''
for i in range(16):
    alphabet2 += chr(ord('a') + i)


class caesar:

    def encode(self, txt, key, language):
        if(language):
            alphabet = alphabet1
        else:
            alphabet = alphabet0
        output = ''
        if (key < 0):
            key = len(alphabet) + key
        for i in txt:
            if (i in alphabet):
                n = (alphabet.find(i) + key) % len(alphabet)
                output += alphabet[n]
            else:
                output += i
        return output

    def decode(self, txt, key, language):
        if (language):
            alphabet = alphabet1
        else:
            alphabet = alphabet0
        key *= -1
        return self.encode(txt, key, language)


class vigenere:

    def encode(self, txt, key, language):
        if (language):
            alphabet = alphabet1
        else:
            alphabet = alphabet0
        counter = 0
        output = ''
        for i in txt:
            if (i in alphabet):
                n = alphabet.find(i) + (alphabet.find(key[counter % len(key)]))
                n %= len(alphabet)
                output += alphabet[n]
                counter += 1
            else:
                output += i
        return (output)

    def decode(self, txt, key, language):
        if (language):
            alphabet = alphabet1
        else:
            alphabet = alphabet0
        key1 = ''
        for i in range(len(key)):
            n = len(alphabet) - alphabet.find(key[i])
            n %= len(alphabet)
            key1 += alphabet[n]
        return self.encode(txt, key1, language)


def train(txt, language):
    if(language):
        alphabet = alphabet1
    else:
        alphabet = alphabet0
    k = 0
    d = {}
    for i in txt:
        if (i in alphabet):
            try:
                d[i] += 1
            except:
                d[i] = 1
            k += 1
    for i in alphabet:
        if (not (i in d)):
            d[i] = 0
    for j in d:
        d[j] *= 100 / k
    return d


def hack(txt, model, language):
    if(language):
        alphabet = alphabet1
    else:
        alphabet = alphabet0
    txtanalysis = train(txt, language)
    minsum = 100 * len(alphabet)
    sum = 0
    minkey = 0
    for key in range(len(alphabet)):
        for i in range(len(alphabet)):
            n = txtanalysis[alphabet[(i + key) % len(alphabet)]]
            n -= model[alphabet[i]]
            sum += n ** 2
        if (minsum > sum):
            minsum = sum
            minkey = key
        sum = 0
    obj = caesar()
    return (obj.decode(txt, minkey, language))


class vernam:

    def encode(self, txt, key):
        output = ''
        counter = 0
        for i in txt:
            if (i in alphabet2):
                n = alphabet2.find(key[counter]) ^ alphabet2.find(i)
                n %= len(alphabet2)
                output += alphabet2[n]
                counter += 1
            elif (i.lower() in alphabet2):
                n = alphabet2.find(key[counter]) ^ alphabet2.find(i.lower())
                n %= len(alphabet2)
                output += (alphabet2[n]).upper()
                counter += 1
            else:
                output += i
        return output

    def decode(self, txt, key):
        return self.encode(txt, key)


def input_file(file):
    try:
        text = codecs.open(file, "r", "utf-8")
        txt = text.read()
        text.close()
    except:
        text = (open(file, "r"))
        txt = text.read()
        text.close()
    return txt


def output_file(file, output_txt):
    text = (open(file, "w"))
    txt = text.write(output_txt)
    text.close()


def read_model(model, language):
    if(language):
        alphabet = alphabet1
    else:
        alphabet = alphabet0
    str = input_file(model)
    model_dict = {}
    number = ""
    for j in range(1, len(str)):
        if ((str[j] in alphabet and str[j-1] == "'" and str[j+1] == "'") or (
            str[j] == "'" and str[j-1] == '"' and str[j+1] == '"'
                ) or (str[j] == "\\" and str[j+1] == "'")):
            i = j
            j += 4
            while (str[j] != ',' and str[j] != '}'):
                number += str[j]
                j += 1
            model_dict[str[i]] = float(number)
            number = ""
    return model_dict


def Encode(cipher, key, inputfile, outputfile, language):
    if(language):
        alphabet = alphabet1
    else:
        alphabet = alphabet0
    if (inputfile):
        try:
            txt = input_file(inputfile)
        except:
            print("I can't read file")
            return None
    else:
        txt = input()
    if (cipher == 'caesar'):
        try:
            caes = caesar()
            inputtxt = caes.encode(txt, int(key), language)
        except:
            print("Key must be integer")
            return None
    elif (cipher == 'vigenere' or cipher == 'vernammod'):
        for i in key:
            if (not (i in alphabet)):
                print("Key must be lowercase")
                return None
        if (cipher == 'vernammod'):
            if (len(key) != len(txt)):
                print("Key must be same lenght with text")
                return None
        vig = vigenere()
        inputtxt = vig.encode(txt, key, language)
    elif (cipher == 'vernam'):
        if (len(key) != len(txt)):
            print("Key must be same lenght with text")
            return None
        for i in key:
            if (not (i in alphabet2)):
                print("Key must consist of first "
                      "16 lowercase letters")
        ver = vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return None
    if (outputfile):
        try:
            output_file(outputfile, inputtxt)
        except:
            print("I can't write in file")
            return None
    else:
        print(inputtxt)


def Decode(cipher, key, inputfile, outputfile, language):
    if(language):
        alphabet = alphabet1
    else:
        alphabet = alphabet0
    if (inputfile):
        try:
            txt = input_file(inputfile)
        except:
            print("I can't read file")
            return None
    else:
        txt = input()
    if (cipher == 'caesar'):
        try:
            int(key)
        except:
            print("Key must be integer")
            return None
        caes = caesar()
        inputtxt = caes.decode(txt, int(key), language)
    elif (cipher == 'vigenere' or cipher == 'vernammod'):
        for i in key:
            if (not (i in alphabet)):
                print("Key must be lowercase")
                return None
        if (cipher == 'vernammod'):
            if (len(key) != len(txt)):
                print("Key must be same lenght with text")
                return None
        vig = vigenere()
        inputtxt = vig.decode(txt, key, language)
    elif (cipher == 'vernam'):
        if (len(key) != len(txt)):
            print("Key must be same lenght with text")
            return None
        for i in key:
            if (not (i in alphabet2)):
                print("Key must consist of first "
                      "16 lowercase letters")
                return None
        ver = vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return None
    if (outputfile):
        try:
            output_file(outputfile, inputtxt)
        except:
            print("I can't write in file")
            return None
    else:
        print(inputtxt)


def Train(text, model, language):
    if (text):
        try:
            txt = input_file(text)
        except:
            print("I can't read file")
            return None
    else:
        txt = input()
    try:
        output_file(model, str(train(txt, language)))
    except:
        print("Not way to output model file")
        return None


def Hack(inputfile, outputfile, modelfile, language):
    try:
        model = read_model(modelfile, language)
    except:
        print("I can't read model file")
        return None
    if (inputfile):
        try:
            txt = input_file(inputfile)
        except:
            print("I can't read file")
            return None
    else:
        txt = input()
    try:
        outputtxt = hack(txt, model, language)
    except:
        print("Problem with model")
        return None
    if (outputfile):
        try:
            output_file(outputfile, outputtxt)
        except:
            print("I can't write in file")
            return None
    else:
        print(outputtxt)


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
    encode.add_argument('--language', dest='language', help='you must write '
                                                            'any string '
                                                            'if cirillic/'
                                                            'and don\'t write '
                                                            'this argument '
                                                            'if latin')

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
    decode.add_argument('--language', dest='language', help='you must write '
                                                            'any string if '
                                                            'cirillic/'
                                                            'and don\'t write '
                                                            'this argument '
                                                            'if latin')

    train = subparsers.add_parser('train', help='train')  # train
    train.add_argument('--text-file', dest='text', help='path '
                                                        'to input text file')
    train.add_argument('--model-file', dest='model', help='output model file')
    train.add_argument('--language', dest='language', help='you must write any'
                                                           ' string if '
                                                           'cirillic/'
                                                           'and don\'t write '
                                                           'this argument '
                                                           'if latin')

    hack = subparsers.add_parser('hack', help='hack')  # hack
    hack.add_argument('--input-file', dest='input', help='path to input file')
    hack.add_argument('--output-file', dest='output', help='path to '
                                                           'output file')
    hack.add_argument('--model-file', dest='model', help='input model file')
    hack.add_argument('--language', dest='language', help='you must write'
                                                          ' any string if'
                                                          ' cirillic/and '
                                                          'don\'t write this'
                                                          ' argument if '
                                                          'latin')

    args = parser.parse_args()
    return args

try:
    args = arguments()
    if (args.work == 'encode'):
        Encode(args.cipher, args.key, args.input, args.output, args.language)
    elif (args.work == 'decode'):
        Decode(args.cipher, args.key, args.input, args.output, args.language)
    elif (args.work == 'train'):
        Train(args.text, args.model, args.language)
    elif (args.work == 'hack'):
        Hack(args.input, args.output, args.model, args.language)
except:
    print("\nWrong input. Try again")
