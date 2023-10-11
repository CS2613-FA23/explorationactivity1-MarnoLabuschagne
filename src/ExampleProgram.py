from pypdf import PdfReader, PdfWriter

# extract rectangles and texts
# remove header and footer
# extract image
def ExtractImages(pdfReader):
    page = pdfReader.pages[0]
    images = []
    
    for page in pdfReader.pages:
        for image in page.images:
            images.append(image)
    return  images
            
def ExtractMetadata(pdfReader):
    meta = pdfReader.metadata
    metadata = []
    
    metadata.append("author:" + str(meta.author))
    metadata.append("creator:" + str(meta.creator))
    metadata.append("producer:" + str(meta.producer))
    metadata.append("subject:" + str(meta.subject))
    metadata.append("title:" + str(meta.title))
    
    return metadata
            
def EncryptFile(pdfReader, fileName, password):
    writer = PdfWriter()
    
    for page in pdfReader.pages:
        writer.add_page(page)
    
    writer.encrypt(password, algorithm="AES-256")
    file = open("output\\encrypted_" + fileName, "wb")
    writer.write(file)
    file.close()

def DecryptFile(pdfReader, fileName, password):
    writer = PdfWriter()
    
    if (pdfReader.is_encrypted):
        pdfReader.decrypt(password)
    
    for page in pdfReader.pages:
        writer.add_page(page)
    
    file = open("output\\decrypted_" + fileName, "wb")
    writer.write(file)
    file.close()

def MergeFiles(fileNames):
    merger = PdfWriter()
    
    for fileName in fileNames:
        merger.append(fileName)
        
    merger.write("output\\MergedPdf.pdf")
    merger.close()

def ExtractText(pdfReader, pagesSelected):
    result = []
    if (len(pagesSelected) == 0):
        for i in range(1, len(pdfReader.pages)+1):
            pagesSelected.append(i)
    print(pagesSelected)
    count = 0
    for i in range(0, len(pdfReader.pages)):
        if (i == pagesSelected[count]-1):
            print("\t{recording page " + str(i) + "}")
            count += 1
            pageText = pdfReader.pages[i].extract_text()
            #print("PAGE TEXT OF PAGE [" + str(i+1) + "]\n" + pageText)
            result.append(pageText)
    return result
        
        

print("Welcome to the pypdf example program!")
while (True):
    print("Please select one of the following options:")
    option = input("\t1. Merge multiple pdfs\n\t2. Read text from a pdf\n\t3. Read Metadata\n\t4. Extract the images from a pdf\n\t5. Decrypt or Encrypt a file\n\t6. Exit\n")

    if (not option.isnumeric()):
        print("\t[INVALID]\n\n")
        print("Please only input a number")
        
    elif (int(option) == 1):
        fileCount = input("\n\tHow many files will you be merging?\n")
        files = []
        for i in range(0, int(fileCount)):
            files.append("input\\" + input("What is the file-name of file [" + str(i+1) + "]?\n"))
        print(files)
        MergeFiles(files)
        
    elif (int(option) == 2):
        fileName = input("What is the file's name?\n")
        reader = PdfReader("input\\" + fileName)
        choice = input("The pdf has [" + str(len(reader.pages)) + "] pages. Do you want to read all of them? [Y/N]\n")
        if (choice == "Y"):
            texts = ExtractText(reader, [])
        elif (choice == "N"):
            numPagesStr = input("Which pages do you want extract? (e.g 1,2,5,7,8)\n")
            numPages = [int(number) for number in numPagesStr.split(",")]
            print(numPages)
            texts = ExtractText(reader, numPages)
        
        file = open("output\\" + fileName[:-4] + ".txt", "w")
        for text in texts:
            try:
                file.write(text + "\n\n\n")
            finally:
                file.write("error encountered\n\n\n")
        file.close()
    
    elif (int(option) == 3):
        fileName = input("What is the file's name?\n")
        reader = PdfReader("input\\" + fileName)
        metadata = ExtractMetadata(reader)
        print ("\nMetadata:")
        for data in metadata:
            print ("\t" + data)
        print()
    
    elif (int(option) == 4):
        fileName = input("What is the file's name?\n")
        reader = PdfReader("input\\" + fileName)
        images = ExtractImages(reader)
        
        count = 0
        for image in images:
            count += 1
            file = open("output\\" + str(count) + image.name, "wb")
            file.write(image.data)
            file.close
        print("Extracted [" + str(count) + "] images\n")
    
    elif (int(option) == 5):
        fileName = input("What is the file's name?\n")
        reader = PdfReader("input\\" + fileName)
        password = input("What is the files password?\n")
        choice = input("Would you like to Encrypt the file? [Y/N]: ")
        if (choice == "Y"):
            EncryptFile(reader, fileName, password)
        else:
            DecryptFile(reader, fileName, password)
    
    elif (int(option) == 6):
        break