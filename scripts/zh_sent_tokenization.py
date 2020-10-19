import sys
import stanza
# stanza.download('zh') 

labels={}

def proc(filename):
	text=[]
	with open(filename) as file:
		currentByte=0
		for line in file:
			cols=line.rstrip().split("\t")
			if len(cols) == 2:
				word=cols[0]	
				label=cols[1]
				text.append(word)
				labels[currentByte]=label

				currentByte+=len(word)


	return (''.join(text))


text=proc(sys.argv[1])
nlp = stanza.Pipeline('zh', processors='tokenize')

doc = nlp(text) 
for i, sentence in enumerate(doc.sentences):
	for j, token in enumerate(sentence.tokens):
		start=token.start_char
		for idx, character in enumerate(token.text):
			char_start=start+idx
			label=""
			if start in labels:
				label=labels[start]
			print("%s\t%s" % (token.text[idx], label))
	print()



