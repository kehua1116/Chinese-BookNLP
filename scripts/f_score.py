import sys, re
from os import listdir
from os.path import isfile, join
#import stanza
#stanza.download('zh')

#labels={}
#
#output_folder = 'fscore/'
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

def generate_tuples(filename):
    tuple_list = []
    with open(filename, encoding='utf-8') as file:
        prev_line = ''
        lines = file.readlines()
        i = 0
        prev_label = lines[0]
        curr_label = lines[0]
        prev_indicator = 0
        not2 = 0
        for k in range(len(lines)):
            #print(i)
            curr_line = lines[k]
#            print("curr_line: %s" %curr_line)
            #print(curr_line)
            cols = curr_line.split('\t')
            #print(cols)
            if len(cols) == 2:
                while prev_label == curr_label and i < len(lines) - 1:
#                    print('prev label:  %s' %prev_label)
#                    print('current label:  %s' %curr_label)
                    if len(lines[i].rstrip().split("\t")) == 2:
                        curr_col = lines[i].rstrip().split("\t")
                        if "-" in curr_col[1]:
                            curr_label = curr_col[1].split("-",1)[1]
                        else:
                            curr_label = curr_col[1]
                        #curr_label = lines[i].rstrip().split("\t")[1]
                    i += 1
#                print('prev_indicator:  %s' %prev_indicator)
#                print('i:  %s' %i)
#                print('current label:  %s' %curr_label)
                if prev_label != 'O' and prev_label != lines[0]:
                    tuple_list.append((prev_indicator, i-1, prev_label))
                prev_label = curr_label
                prev_indicator = i
    return tuple_list
        
gold = generate_tuples(sys.argv[1])
system = generate_tuples(sys.argv[2])
print(gold)

def f_score(gold, system):
    gold_length = len(gold)
    system_length = len(system)
    same_num = 0
    for gold_item in gold:
        for system_item in system:
            if gold_item == system_item:
                same_num += 1
    precision = same_num / len(system)
    recall = same_num / len(gold)
    fscore = 2 * (precision * recall) / (precision + recall)
    print("precision:  %s" % precision)
    print("recall:  %s" % recall)
    return fscore
        
a = [(1,2,'PER'), (7,7,'ORG'), (5,5,'PER')]
b = [(1,1,'PER'), (5,5,'PER'), (7,7,'ORG')]
#print(f_score(gold, system))


















#nlp = stanza.Pipeline('zh', processors='tokenize')
#
#def f_score(folder):
#    all_files = [f for f in listdir(folder) if isfile(join(folder, f))]
#    for filename in all_files:
#        #print(isfile(filename))
#        if filename.endswith("txt"):
#            name = re.sub("\.txt$", "", filename.split("/")[-1])
#            completeName = join(output_folder, name)
#            new_f = open(completeName + '_BIO.txt', "w")
#            text=proc(folder + '/' + filename)
#            doc = nlp(text)
#            for i, sentence in enumerate(doc.sentences):
#                for j, token in enumerate(sentence.tokens):
#                    start=token.start_char
#                    for idx, character in enumerate(token.text):
#                        char_start=start+idx
#                        label=""
#                        if start in labels:
#                            label=labels[start]
#                        if (token.text[idx] != '\n' and token.text[idx] != ' '):
#                            new_f.write("%s\t%s" % (token.text[idx], label))
#                            new_f.write('\n')
#                new_f.write('\n')
#            new_f.close()
#
#write_bio(sys.argv[1])
