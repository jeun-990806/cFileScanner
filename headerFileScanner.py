import os
import re

import fileManagement
import tools

headerFilePath = 'header_files/'


class HeaderFileScanner:
    rootPath = ''
    defaultRootPath = ''
    directoryList = []

    targetHeaderFiles = []
    notScannedHeaderFiles = []
    scannedHeaderFiles = []

    symbolicConstantsData = {}
    structureData = {}

    defineStatementRE = '#[\s]*(?:define|DEFINE)[^\n]*'
    definePartRE = '#[\s]*(?:define|DEFINE)[\s]*'
    symbolicConstantRE = '[A-Z]+[A-Z_0-9]+'
    headerFileRE = '<[\S]+\.h>'

    def __init__(self, path=None, targetHeaderFiles=None):
        if path is not None:
            self.rootPath = path

        if targetHeaderFiles is not None:
            self.targetHeaderFiles = targetHeaderFiles
        else:
            # find all targeted directories
            self.directoryList = [self.rootPath]
            currentDirIndex = 0
            while True:
                if currentDirIndex >= len(self.directoryList):
                    break
                currentDir = self.directoryList[currentDirIndex]
                newDirectoryList = [currentDir + directory for directory in fileManagement.getDirectoryList(currentDir)]
                self.directoryList += newDirectoryList
                currentDirIndex += 1

            # find all targeted header files
            for directory in self.directoryList:
                self.targetHeaderFiles += [directory + fileName for fileName in fileManagement.getFileList(directory)]

    def addIncludedHeaderFiles(self):
        for header in self.targetHeaderFiles:
            for included in re.findall(self.headerFileRE, ''.join(fileManagement.openFile(header))):
                included = self.rootPath + included.replace('<', '').replace('>', '')
                if os.path.isfile(included):
                    if included not in self.targetHeaderFiles:
                        self.targetHeaderFiles.append(included)
                else:
                    print('addIncludeHeaderFiles(): there is no ' + included)

    def scanSymbolicConstants(self):
        for header in self.targetHeaderFiles:
            print('scanSymbolicConstants(): scan ' + header)
            for line in fileManagement.openFile(header):
                for statement in re.findall(self.defineStatementRE, line):
                    statement = re.sub(self.definePartRE, '', statement).strip()
                    symbolicConstant = re.findall(self.symbolicConstantRE, statement)
                    if header not in self.symbolicConstantsData.keys():
                        self.symbolicConstantsData[header] = []
                    self.symbolicConstantsData[header] += symbolicConstant

    '''    def getStructureList(contents):
        structureRE = '(?:\ntypedef |\n)struct[^{;]*(?:\{[^}]*\}|)[^;]*;'
        fullText = ''
        for content in contents:
            fullText += content
        return re.findall(structureRE, tools.removeComments(fullText))

    def getStructureName(struct):
        if struct.replace('\n', '').startswith('typedef'):
            return struct.split('}')[-1].replace(';', '').strip()
        else:
            return struct.split('{')[0].replace('\n', '').replace(';', '').strip()

    def getStructureContents(struct):
        structContentRE = '{[\S\s]+};'
        result = re.findall(structContentRE, struct)
        if len(result) != 0:
            return result[0]

    def getStructureDataNameList(struct):
        fieldRE = '[a-zA-Z0-9][^;]+;'
        if getStructureContents(struct) is not None:
            return [getFieldData(field) for field in re.findall(fieldRE, getStructureContents(struct))
                    if getFieldData(field) is not None]

    def getFieldData(field):
        field = field.replace('\t', ' ')
        if not checkFieldType(field):
            fieldName = field[field.rfind(' ') + 1:].replace(';', '')
            fieldType = field[:field.rfind(' ')]
            return fieldType, fieldName

    def checkFieldType(field):
        wrongCase = '~!@#$%^&+=|\\\?\[\]{}():;\'"`<>.'
        argumentsRE = '[(](?:[(][^0-9' + wrongCase + '][^;]+[)]|[^' + wrongCase + '])*[)]'
        if len(re.findall(argumentsRE, field)) == 0:
            return False
        else:
            return True'''