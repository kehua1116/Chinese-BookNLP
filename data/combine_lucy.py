import sys, re
from os import listdir
from os.path import isfile, join

def combine(folder):
    filenames  = ['book_11_text.txt','book_18_text.txt','book_6_text.txt','book_10_text.txt',
'book_12_text.txt','book_13_text.txt','book_4_text.txt','book_1_text.txt',
'book_8_text.txt','book_16_text.txt','book_9_text.txt','book_golden_age.txt',
'book_border_town.txt','book_to_live.txt','book_3body.txt',
'book_15_text.txt','book_2_text.txt','book_3_text.txt','book_jerusalem.txt',
'book_14_text.txt']
    
    out = ""
    for i in range(len(filenames)):
        with open(folder + '/' + filenames[i], encoding='utf-8') as infile: 
            content = infile.read()
            out = out + content
        out = out + "\n"
        print(filenames[i])
    return out

all_books = combine('entire_book_after_OCR')
with open('all_BIOs.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(all_books)

# name_list = ['book_11_text.txt','book_18_text.txt','book_6_text.txt','book_10_text.txt',
# 'book_12_text.txt','book_13_text.txt','book_4_text.txt','book_1_text.txt',
# 'book_8_text.txt','book_16_text.txt','book_9_text.txt','book_golden_age.txt',
# 'book_border_town.txt','book_to_live.txt','book_3body.txt',
# 'book_15_text.txt','book_2_text.txt','book_3_text.txt','book_jerusalem_text.txt',
# 'book_14_text.txt']
