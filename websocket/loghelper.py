

def logLine(fileName : str, line : str):
    file_object = open(fileName, 'a+')
    file_object.write("%s\n" % line)
    file_object.close()