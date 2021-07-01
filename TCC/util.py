import nltk
import os
import os.path
import nltk.corpus
import pickle
import pprint

def tagger():
    tagged_sents = nltk.corpus.mac_morpho.tagged_sents()
    file = open('E:\\TCC\\RedacoesTagged.txt', 'r', encoding='utf-8')
    read = file.read()
    tokens = nltk.word_tokenize(read)
    tagger = nltk.tag.UnigramTagger(tagged_sents)
    fileWrite = open('E:\\TCC\\RedacoesTagged.txt', 'w', encoding='utf-8')
    
    # for token in tokens:
    #     if token == '':
    #          tags = tagger.tag(tokens)
    tags = tagger.tag(tokens)


    for tag in zip(tags):
        string = ''.join('({0}, {1})'.format(item[0], item[1])for item in tag)
        fileWrite.write(string)
    return print(tokens)

def pickleGenerator():
    file = open('E:\\TCC\\RedacoesTagged.txt', 'r', encoding='utf-8')
    read = file.read()
    pickleFile = open('E:\\TCC\\Tagged_sents.pickle', 'wb')

    for item in read:
        print(item)
        pickle.dump(item, pickleFile)

    return 'ok'

def pickleReader():
    objects = []
    with(open('E:\\TCC\\dataAP\\user_defined_tagger.pickle', 'rb')) as pf:
        while True:
            try:
                objects.append(pickle.load(pf))
            except EOFError:
                break
    return print(objects)

pickleReader()
