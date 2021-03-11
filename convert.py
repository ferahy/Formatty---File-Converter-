import os
from time import strftime
from win32com import client

# Counts the number of files
def numOfFiles(directory):
    count = 0
    for file in os.listdir(directory):
        if (file.endswith('.doc') or file.endswith('.docx')):
            count += 1
    return count

# Create a new directory 
def createFolder(directory):
    if not os.path.exists(directory + '\\PDFsDirectory'):
        os.makedirs(directory + '\\PDFsDirectory')
		
if __name__ == "__main__":
    print('\nThis program will overwrite any existing PDF files')
	
    directory = os.getcwd()
	
    if numOfFiles(directory) == 0:
        print('no files to convert, we are sorry :(')
        exit(1)
		
    createFolder(directory)
	
    print('Conversion started... \n')
	
    # save pdf
    try:
        word = client.DispatchEx('Word.Application')
        for file in os.listdir(directory):
            if (file.endswith('.doc') or file.endswith('.docx')):
                ending = ""
                if file.endswith('.doc'):
                    ending = '.doc'
                if file.endswith('.docx'):
                    ending = '.docx'
                new_name = file.replace(ending,r".pdf")
                in_file = os.path.abspath(directory + '\\' + file)
                new_file = os.path.abspath(directory + '\\PDFs' + '\\' + new_name)
                doc = word.Documents.Open(in_file)
                print(new_name)
                doc.SaveAs(new_file,FileFormat = 17)
                doc.Close()
    except :
        print("Error: Aborting")
    finally:
        word.Quit()
