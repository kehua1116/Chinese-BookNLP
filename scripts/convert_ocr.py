import sys, re
from os import listdir
from os.path import isfile, isdir, join
import os

def read_texts(folder, id):
	texts={}
	onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
	for filename in onlyfiles:
		if filename.endswith("txt"):
			name=int(re.sub("\.txt$", "", filename.split("/")[-1]))
			with open(folder + '/' + filename,  encoding='utf-8') as file:
				data=file.read()
				texts[name]=data
	return texts[id]

def read_anns(filename):
	anns=[]
	with open(filename, encoding='utf-8') as file:
		file.readline()
		for line in file:
			cols=line.rstrip().split("\t")

			chunk_id=int(cols[0])
			mention=cols[3]

			anno=cols[2].split(" ")
			label=anno[0]

			if label == "OCR_ERROR":
				continue

			start=int(anno[1])
			print(anno)
			end=int(anno[2])
			anns.append((chunk_id, label, start, end, mention))

	return anns


def generate_bio(new_chunk_name, chunk, anns, id):
	new_f = open(new_chunk_name, "w")
	for j in range(len(chunk)):
	    each_token = chunk[j]
	    is_BI = False
	    if chunk[j] != '\n':
		    new_f.write(chunk[j])
		    new_f.write('\t')
	    for chunk_id, label, start, end, mention in anns:
	        if chunk_id == id:
	            if j < start:
	                continue
	            elif j == start:
	                new_f.write('B-' + label + '\n')
	                is_BI = True
	                break
	            elif j < end:
	                new_f.write('I-' + label + '\n')
	                is_BI = True
	                break
	            else:
	                continue
	    if is_BI == False and chunk[j] == '\n':
	    	new_f.write('\n')
	    elif is_BI == False:
	    	new_f.write('O' + '\n')

	new_f.close()
	return new_f


def replace_ocr_error(ann_folder, bio_folder):
	bio_text = {}
	ann_f = [f for f in listdir(ann_folder) if isfile(join(ann_folder, f))]
	bio_f = [f for f in listdir(bio_folder) if isfile(join(bio_folder, f))]
	for ann_file in ann_f:
		if ann_file.endswith("ann"):
			name=int(re.sub("\.ann$", "", ann_file.split("/")[-1]))
			with open(ann_folder + '/' + ann_file,  encoding='utf-8') as file:
				file.readline()
				count = 0
				for line in file:					
					if "AnnotatorNotes" in line:
						id = line.split('\t')[1].split(' ')[1]
						new_content = line.split('\t')[2][0:-1]
						with open(ann_folder + '/' + ann_file,  encoding='utf-8') as file2:
							for line2 in file2:
								if "AnnotatorNotes" not in line2 and id == line2.split('\t')[0]:
									start = int(line2.split('\t')[1].split(' ')[1])
									end = int(line2.split('\t')[1].split(' ')[2])
									bio_text[name] = replace_string(bio_folder, bio_f[name], start + count, end + count, new_content)
									if 'DEL' in new_content:
										count += (0 - (end - start))
									else:
										count += (len(new_content) - (end- start))
									print(count)
								



def replace_string(bio_folder, bio, start, end, new_content):
	print(bio)
	file = open(bio_folder + '/' + bio, "r", encoding='utf-8')
	lines= file.readlines()
	file.close()
	for i in range(start, end):
		print(lines[start])
		del lines[start]
	if 'DEL' not in new_content:
		for i in range(len(new_content)):
			lines.insert(start + i, new_content[i] + "	O\n")

	# file = open(bio_folder + '/' + bio, "w", encoding='utf-8')
	# file.writelines(lines)
	# file.close()
	return file



# To run on 1_text:
# Download 1_text.coref as tsv (1_text.coref.tsv)
# python test.py original\ BRAT\ files/1_text 1_text.coref.tsv
# id = 1
# chunk = read_texts(sys.argv[1], id)
# anns=read_anns(sys.argv[2])


# new_chunk_name = "text_8_chunk_1_BIO.txt"
# generate_bio(new_chunk_name, chunk, anns, id)
#sys.argv[1]: .ann file folder
#sys.argv[2]:BIO notation text folder (each chunk is a file)
#converted_texts=replace_ocr_error(sys.argv[1], sys.argv[2])





def replace_ocr_error2(original_brat_files):
	ann_folders = [f for f in listdir(original_brat_files) if isdir(join(original_brat_files, f)) ]
	for ann_folder in ann_folders:
		text_text = {}
		ann_f = [f for f in listdir(join(original_brat_files, ann_folder)) if f.endswith("ann")]
		text_f = [f for f in listdir(join(original_brat_files, ann_folder)) if f.endswith("txt")]
		for ann_file in ann_f:
			name=int(re.sub("\.ann$", "", ann_file.split("/")[-1]))
			with open(original_brat_files + '/' + ann_folder + '/' + ann_file,  encoding='utf-8') as file:
				file.readline()
				count = 0
				for line in file:					
					if "AnnotatorNotes" in line:
						id = line.split('\t')[1].split(' ')[1]
						new_content = line.split('\t')[2][0:-1]
						with open(original_brat_files + '/' + ann_folder + '/' + ann_file,  encoding='utf-8') as file2:
							for line2 in file2:
								if "AnnotatorNotes" not in line2 and id == line2.split('\t')[0]:
									start = int(line2.split('\t')[1].split(' ')[1])
									end = int(line2.split('\t')[1].split(' ')[2])
									text_text[name] = replace_string2(original_brat_files, ann_folder, text_f[name], start + count, end + count, new_content)
									if 'DEL' in new_content:
										count += (0 - (end - start))
									else:
										count += (len(new_content) - (end- start))
									print(count)
		
		combine(original_brat_files, ann_folder)

							



def replace_string2(original_brat_files, ann_folder, text, start, end, new_content):
	print(join(ann_folder, text))
	file = open(join(original_brat_files, ann_folder, text), "r", encoding='utf-8')
	lines= file.readlines()
	all_text = ""
	for line in lines:
		all_text = all_text + line
	file.close()

	print(all_text[start:end])
	all_text = all_text[:start] + "" + all_text[end:]
	if 'DEL' not in new_content:
		all_text = all_text[:start] + new_content + all_text[start:]
		
	file = open(join(original_brat_files, ann_folder, text) , "w", encoding='utf-8')
	file.writelines(all_text)
	file.close()
	return file


def combine(original_brat_files, ann_folder):
	#folder = 'entirebook_after_OCR/' + original_brat_files
	if "border" in ann_folder or "golden" in ann_folder or "jerusalem" in ann_folder:
		return 

	filenames = [str(i) + '.txt' for i in range(10)] 
	print(join(ann_folder, filenames[0]))
	with open('book_' + ann_folder + '.txt', 'w', encoding='utf8') as outfile: 
	    for i in range(len(filenames)):
	        with open(join(original_brat_files, ann_folder, filenames[i]), encoding='utf-8') as infile: 
	            outfile.write(infile.read()) 

	        outfile.write("\n") 
	outfile.close()
	print("combined " + ann_folder)

converted_texts=replace_ocr_error2(sys.argv[1])




