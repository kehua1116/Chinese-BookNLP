import sys,re
from os import listdir
from os.path import isfile, join
import stanza
# stanza.download('zh') 

#file = open(sys.argv[1], "r", encoding='utf-8')
#text = file.read()
nlp = stanza.Pipeline('zh', processors='tokenize, ner')
#doc = nlp(text)

output_folder = 'stanza_output/'

def proc(filename):
    text=[]
    with open(filename, encoding='utf-8') as file:
        currentByte=0
        for line in file:
            cols=line.rstrip().split("\t")
            if len(cols) == 2:
                word=cols[0]
                word = word.replace(" ", "")
                label=cols[1]
                text.append(word)

    return (''.join(text))

def convert_to_bio(folder):
    all_files = [f for f in listdir(folder) if isfile(join(folder, f))]
    for filename in all_files:
        if filename.endswith("txt"):
            name = re.sub("\.txt$", "", filename.split("/")[-1])
            completeName = join(output_folder, name)
            new_f = open(completeName + '_stanza.txt', "w")
            #text=proc(folder + '/' + filename)
            file = open(folder + '/' + filename, "r", encoding='utf-8')
            text = file.read()
            doc = nlp(text)
            for i, sentence in enumerate(doc.sentences):
                for j, token in enumerate(sentence.tokens):
                    start=token.start_char
                    text = token.text.replace(" ", "")
                    for idx, character in enumerate(text):
                        label=token.ner
                        print(text + '!')
                        new_f.write("%s\t%s" % (text[idx], label))
                        new_f.write('\n')
                new_f.write('\n')
            new_f.close()
         
convert_to_bio(sys.argv[1])


#labels={}
#
#def proc(filename):
#	text=[]
#	with open(filename) as file:
#		currentByte=0
#		for line in file:
#			cols=line.rstrip().split("\t")
#			if len(cols) == 2:
#				word=cols[0]
#				label=cols[1]
#				text.append(word)
#				labels[currentByte]=label
#
#				currentByte+=len(word)
#
#
#	return (''.join(text))
#
#
#text=proc(sys.argv[1])
#nlp = stanza.Pipeline('zh', processors='tokenize')
#
#doc = nlp(text)
#for i, sentence in enumerate(doc.sentences):
#	for j, token in enumerate(sentence.tokens):
#		start=token.start_char
#		for idx, character in enumerate(token.text):
#			char_start=start+idx
#			label=""
#			if start in labels:
#				label=labels[start]
#			print("%s\t%s" % (token.text[idx], label))
#	print()
#
#

