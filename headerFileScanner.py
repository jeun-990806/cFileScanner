import os
import re

import fileManagement
import tools


class HeaderFileScanner:
    rootPath = 'header_files/'
    __defaultDestination = ''
    __directoryList = []

    targetHeaderFiles = []
    __notScannedHeaderFiles = []
    __scannedHeaderFiles = []

    __symbolicConstantsData = {}
    __structureData = {}

    __defineStatementRE = '#[\s]*(?:define|DEFINE)[^\n]*'
    __definePartRE = '#[\s]*(?:define|DEFINE)[\s]*'
    __symbolicConstantRE = '[A-Z]+[A-Z_0-9]+'
    __headerFileRE = '<[\S]+\.h>'
    __structureRE = '(?:typedef |)struct(?: [a-zA-Z0-9_]*|)(?:\{[^}]*\}|)[^;]*;'
    __fieldVariableRE = '[a-zA-Z_][a-zA-Z0-9_]+[\s]+[a-zA-Z_][a-zA-Z0-9_]+;'
    __structureNameRE = '[a-zA-Z0-9_]+'

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
            for included in re.findall(self.__headerFileRE, ''.join(fileManagement.openFile(header))):
                included = self.rootPath + included.replace('<', '').replace('>', '')
                if os.path.isfile(included):
                    if included not in self.targetHeaderFiles:
                        self.targetHeaderFiles.append(included)
                else:
                    print('addIncludeHeaderFiles(): there is no ' + included)

    def scanSymbolicConstants(self, destination=None):
        if destination is None:
            destination = self.__defaultDestination
        else:
            if not destination.endswith('/'):
                destination += '/'
        for header in self.targetHeaderFiles:
            print('scanSymbolicConstants(): scan ' + header)
            fileContents = fileManagement.openFile(header)
            if fileContents is None:
                self.__notScannedHeaderFiles.append(header)
                continue
            for line in fileManagement.openFile(header):
                for statement in re.findall(self.__defineStatementRE, line):
                    statement = re.sub(self.__definePartRE, '', statement).strip()
                    symbolicConstant = re.findall(self.__symbolicConstantRE, statement)
                    if header not in self.__symbolicConstantsData.keys():
                        self.__symbolicConstantsData[header] = []
                    self.__symbolicConstantsData[header] += symbolicConstant
            self.__scannedHeaderFiles.append(header)
            fileManagement.saveData(self.__symbolicConstantsData[header], destination + header[header.rfind('/') + 1:header.rfind('.')] + '.list')

    def scanStructures(self, destination=None):
        if destination is None:
            destination = self.__defaultDestination
        else:
            if not destination.endswith('/'):
                destination += '/'
        for header in self.targetHeaderFiles:
            print('scanStructures(): scan ' + header)
            for structure in re.findall(self.__structureRE, tools.removeComments(' '.join(fileManagement.openFile(header)))):
                # structure name
                if structure.replace('\n', '').startswith('typedef'):
                    structureName = structure.split('}')[-1].replace(';', '').strip().replace(' ', '_')
                else:
                    structureName = structure.split('{')[0].replace('\n', '').replace(';', '').strip().replace(' ', '_')
                # check structure name
                if re.fullmatch(self.__structureNameRE, structureName) is None:
                    continue
                # fields data
                fields = [field.replace('\t', ' ') for field in re.findall(self.__fieldVariableRE, structure)]
                self.__structureData[structureName] = [(field.split(' ')[0], field.split(' ')[1]) for field in fields if len(field.split(' ')) >= 2]
                fileManagement.saveData(self.__structureData[structureName], destination + structureName + '.list')