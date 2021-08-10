import os
import pickle
import csv
import sys

sys.setrecursionlimit(10000)


def getFileList(path):
    if not os.path.isdir(path):
        print('getFileList(): there is no such directory (' + path + ')')
        return
    return [file for file in os.listdir(path) if os.path.isfile(path + file)]


def getDirectoryList(path):
    if not os.path.isdir(path):
        print('getDirectoryList(): there is no such directory (' + path + ')')
        return
    return [directory + '/' for directory in os.listdir(path) if os.path.isdir(path + directory)]


def openFile(path):
    if os.path.isfile(path):
        f = open(path, 'r')
        try:
            lines = f.readlines()
        except:
            print('openFile(): cannot open file (' + path + ')')
            lines = None
        f.close()
        return lines
    else:
        print('openFile(): there is no such file (' + path + ')')
        return []


def saveData(data, path):
    dirName = path[:path.rfind('/')]
    if len(dirName) != 0 and not os.path.isdir(dirName):
        os.mkdir(dirName, mode=0o777)
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    f.close()


def openData(path):
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        with open(path, 'rb') as f:
            result = pickle.load(f)
        f.close()
    else:
        if path.endswith('.dict'):
            result = {}
        if path.endswith('.list'):
            result = []
    return result


def saveDataToCsv(data, path):
    if type(data) == '<class \'list\'>':
        print('saveDataToCsv(): data must be list type')
    dirName = path[:path.rfind('/')]
    if len(dirName) != 0 and not os.path.isdir(dirName):
        os.mkdir(dirName, mode=0o777)
    with open(path, 'wb') as f:
        w = csv.writer(f)
        for elem in data:
            w.writerow([elem])
    f.close()
