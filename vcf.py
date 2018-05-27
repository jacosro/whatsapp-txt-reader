import re


class VCFParser():

    def __init__(self, file):
        self.file = file

    def setFile(self, newFile):
        self.file = newFile

    def getNumber(self):
        try:
            with open(self.file, 'r') as f:
                search = re.compile(".*TEL.*:(.*)")
                for line in f:
                    match = search.match(line)
                    if match:
                        return match.group(1)
        except IOError:
            print("Error reading file: " + self.file)
        return ""
