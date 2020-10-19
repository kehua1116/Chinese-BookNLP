#python combine.py

folder = 'original_brat_files/to_live'
filenames = [str(i) + '.txt' for i in range(10)] 
  
# Open file3 in write mode 
with open('book_to_live.txt', 'w') as outfile: 
  
    # Iterate through list 
    for i in range(len(filenames)):
    
        # Open each file in read mode 
        with open(folder + '/' + filenames[i], encoding='utf-8') as infile: 
            # read the data from file1 and 
            # file2 and write it in file3 
            print(filenames[i])
            outfile.write(infile.read()) 
  
        # Add '\n' to enter data of file2 
        # from next line 
        outfile.write("\n") 