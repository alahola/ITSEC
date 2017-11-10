def prepareFile(file_name):
	readFile = open(file_name+".txt", "r+")
	name = file_name+"_compressed.txt"
	bufferData = readFile.read().lower()
	for stringcounter in range(0, len(bufferData)):
			if not bufferData[stringcounter].isalpha():
				bufferData = bufferData.replace(bufferData[stringcounter], '$')
	bufferData = bufferData.replace('$', '')
	readFile.close()
	writeFile = open(name, "wb")
	writeFile.write(bufferData)
	readFile.close()
	writeFile.close()

def compressFile(path):
    file = open(path)
    message = ""

    while True:
        c = file.read(1)
        if not c:
            break
        if c.isalpha():
            message += c.lower()

    return message