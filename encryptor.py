import argparse

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet2 = ''
for i in range(16):
    alphabet2 += chr(ord('a')+i)

class caesar:

    def encode(self, txt, key):
        output = ''
        if (key < 0):
            key = len(alphabet) + key
        for i in txt:
            if (i in alphabet):
                output += alphabet[(alphabet.find(i) + key) % len(alphabet)]
            elif(i.lower() in alphabet):
                output += (alphabet[(alphabet.find(i.lower()) + key) % len(alphabet)]).upper()
            else:
                output += i
        return output

    def decode(self, txt, key):
        key *= -1
        return self.encode(txt, key)


alphabet = 'abcdefghijklmnopqrstuvwxyz'


class vigenere:

    def encode(self, txt, key):
        counter = 0
        output = ''
        for i in txt:
            if (i in alphabet):
                output += alphabet[(alphabet.find(i) + (alphabet.find(key[counter % len(key)]))) % len(alphabet)]
                counter += 1
            elif (i.lower() in alphabet):
                output += (
                alphabet[(alphabet.find(i.lower()) + (alphabet.find(key[counter % len(key)]))) % len(alphabet)]).upper()
                counter += 1
            else:
                output += i
        return (output)

    def decode(self, txt, key):
        key1 = ''
        for i in range(len(key)):
            key1 += alphabet[(len(alphabet) - alphabet.find(key[i])) % len(alphabet)]
        return self.encode(txt, key1)

def train(txt):
    k = 0
    d = {}
    for i in txt:
        if (i.lower() in alphabet):
            try:
                d[i.lower()] += 1
            except:
                d[i.lower()] = 1
            k += 1
    for i in alphabet:
        if(not (i in d)):
            d[i] = 0
    for j in d:
        d[j] *= 100/k
    return d

def hack(txt, model):
    txtanalysis = train(txt)
    minsum = 100 * len(alphabet)
    sum = 0
    minkey = 0
    for key in range(len(alphabet)):
        for i in range(len(alphabet)):
            sum += ((txtanalysis[alphabet[(i + key) % len(alphabet)]] - model[alphabet[i]]))**2
        if(minsum > sum):
            minsum = sum
            minkey = key
        sum = 0
    obj = caesar()
    return(obj.decode(txt, minkey))



class vernam:

    def encode(self, txt, key):
        output = ''
        counter = 0
        for i in txt:
            if(i in alphabet2):
                output += alphabet2[(alphabet2.find(key[counter]) ^ alphabet2.find(i)) % len(alphabet2)]
                counter += 1
            elif(i.lower() in alphabet2):
                output += (alphabet2[(alphabet2.find(key[counter]) ^ alphabet2.find(i.lower())) % len(alphabet2)]).upper()
                counter += 1
            else:
                output += i
        return output

    def decode(self, txt, key):
        return self.encode(txt, key)

def input_file(file):
    text = (open(file, "r"))
    txt = text.read()
    text.close()
    return txt

def output_file(file, output_txt):
    text = (open(file, "w"))
    txt = text.write(output_txt)
    text.close()

def read_model(model):
    str = input_file(model)
    model_dict = {}
    number = ""
    for j in range(len(str)):
        if (str[j] in alphabet):
            i = j
            while(str[j+4] != ',' and str[j+4] != '}'):
                number += str[j+4]
                j += 1
            model_dict[str[i]] = float(number)
            number = ""
    return model_dict

def Encode(cipher, key, inputfile, outputfile):
    if(inputfile!=None):
        try:
           txt = input_file(inputfile)
        except:
            print("I can't read file")
            return
    else:
        txt = input()
    if(cipher == 'caesar'):
        try:
            caes = caesar()
            inputtxt = caes.encode(txt, int(key))
        except:
            print("Key must be integer")
            return
    elif(cipher == 'vigenere' or cipher == 'vernammod'):
        for i in key:
            if(not(i in alphabet)):
                print("Key must be lowercase")
                return
        if(cipher == 'vernammod'):
            if(len(key)!=len(txt)):
                print("Key must be same lenght with text")
        vig = vigenere()
        inputtxt = vig.encode(txt, key)
    elif(cipher == 'vernam'):
        if (len(key) != len(txt)):
            print("Key must be same lenght with text")
        for i in key:
            if(not(i in alphabet)):
                print("Key must consist of first 16 lowercase letters")
        ver = vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return
    if (outputfile != None):
        try:
            output_file(inputtxt, outputfile)
        except:
            print("I can't write in file")
            return
    else:
        print(inputtxt)

def Decode(cipher, key, inputfile, outputfile):
    if(inputfile!=None):
        try:
           txt = input_file(inputfile)
        except:
            print("I can't read file")
            return
    else:
        txt = input()
    if(cipher == 'caesar'):
        try:
            int(key)
        except:
            print("Key must be integer")
            return
        caes = caesar()
        inputtxt = caes.decode(txt, int(key))
    elif(cipher == 'vigenere' or cipher == 'vernammod'):
        for i in key:
            if(not(i in alphabet)):
                print("Key must be lowercase")
                return
        if(cipher == 'vernammod'):
            if(len(key)!=len(txt)):
                print("Key must be same lenght with text")
        vig = vigenere()
        inputtxt = vig.decode(txt, key)
    elif(cipher == 'vernam'):
        if (len(key) != len(txt)):
            print("Key must be same lenght with text")
        for i in key:
            if(not(i in alphabet)):
                print("Key must consist of first 16 lowercase letters")
        ver = vernam()
        inputtxt = ver.decode(txt, key)
    else:
        print("Wrong cipher")
        return
    if(outputfile != None):
        try:
            output_file(inputtxt, outputfile)
        except:
            print("I can't write in file")
            return
    else:
        print(inputtxt)

def Train(text, model):
    if (text != None):
        try:
            txt = input_file(text)
        except:
            print("I can't read file")
            return
    else:
        txt = input()
    try:
        output_file(model, str(train(txt)))
    except:
        print("Not way to output model file")
        return


def Hack(inputfile, outputfile, modelfile):
    try:
        model = read_model(modelfile)
    except:
        print("I can't read model file")
        return
    if (inputfile != None):
        try:
            txt = input_file(inputfile)
        except:
            print("I can't read file")
            return
    else:
        txt = input()
    try:
        outputtxt = hack(txt, model)
    except:
        print("Problem with model")
        return
    if(outputfile == None):
        print(outputtxt)
    else:
        try:
            output_file(outputfile, outputtxt)
        except:
            print("I can't write in file")


def arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='work', help='What does the program do')

    encode = subparsers.add_parser('encode', help='encode') #encode
    encode.add_argument('--cipher', help='cipher - caesar/vigenere/vernammod/vernam')
    encode.add_argument('--key', dest='key',help='key'
                                                 '/integer for caesar'
                                                 '/string lowercase letters for vigenere'
                                                 '/file lenght string lowercase letters for vernammod'
                                                 '/file lenght string with first 16 lowercase letters for vernam')
    encode.add_argument('--input-file', dest='input', help='path to input file')
    encode.add_argument('--output-file', dest='output', help='path to output file')

    decode = subparsers.add_parser('decode', help='decode') #decode
    decode.add_argument('--cipher', help='cipher - caesar/vigenere/vernammod/vernam')
    decode.add_argument('--key', dest='key', help='key'
                                                  '/integer for caesar'
                                                  '/string lowercase letters for vigenere'
                                                  '/file lenght string lowercase letters for vernammod'
                                                  '/file lenght string with first 16 lowercase letters for vernam')
    decode.add_argument('--input-file', dest='input', help='path to input file')
    decode.add_argument('--output-file', dest='output', help='path to output file')

    train = subparsers.add_parser('train', help='train') #train
    train.add_argument('--text-file', dest='text', help='path to input text file')
    train.add_argument('--model-file', dest='model', help='output model file')

    hack = subparsers.add_parser('hack', help='hack') #hack
    hack.add_argument('--input-file', dest='input', help='path to input file')
    hack.add_argument('--output-file', dest='output', help='path to output file')
    hack.add_argument('--model-file', dest='model', help='input model file')

    args = parser.parse_args()
    return args


args = arguments()
if(args.work == 'encode'):
    Encode(args.cipher, args.key, args.input, args.output)
elif(args.work == 'decode'):
    Decode(args.cipher, args.key, args.input, args.output)
elif (args.work == 'train'):
    Train(args.text, args.model)
elif (args.work == 'hack'):
    Hack(args.input, args.output, args.model)


