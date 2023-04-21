#Imports
from glob import glob
import re
import numpy as np

def parseHtmls(html):
    HtmlFile = open(html, 'r', encoding='utf-8')
    wholeFile =  HtmlFile.readlines()
    return wholeFile

def saveHtmls(htmls, htmlsFiles):
    for n, html in enumerate(htmls):
        HtmlFile = open(htmlsFiles[n], 'w+', encoding='utf-8')
        for line in htmls[html]:
            HtmlFile.write(line)
        HtmlFile.close()
    HtmlFile = open('index.html', 'w+', encoding='utf-8')
    for line in htmls['index.html']:
        HtmlFile.write(line)
    HtmlFile.close()

def parseEu4():
    #Get Tag File Info
    tagFiles = glob('Eu4/common/country_tags/*.txt')
    tagSet = []
    for tagFile in tagFiles:
        with open(tagFile, 'r', encoding='utf-8') as f:
            tagSet.append(f.readlines())
            f.close()

    #Filter to Relevant Info
    tags = []
    copyTagSet = tagSet
    for n, tagList in enumerate(copyTagSet):
        for tag in tagList:
            if not re.match(r'^#', tag):
                tags.append(tag[:3])

    #Get Province File Info
    provFiles = glob('Eu4/history/provinces/*.txt')
    owners = {}
    for provFile in provFiles:
        #Get id
        id = re.sub('\D', '', provFile[3:])
        provLines = []
        with open(provFile, 'r', encoding='utf-8') as prov:
            provLines.append(prov.readline())
            prov.close()
        for line in provLines:
            if not line.strip():
                continue
            try:
                if re.match(r'^owner=\w{1,99}', line):
                    owners[line[6:9]]+= [id]
                elif re.match(r'^owner = \w{1,99}', line):
                    owners[line[8:11]]+= [id]
                elif re.match(r'^owner= \w{1,99}', line):
                    owners[line[7:10]]+= [id]
                elif re.match(r'^owner =\w{1,99}', line):
                    owners[line[7:10]]+= [id]
            except:
                if re.match(r'^owner=\w{1,99}', line):
                    owners[line[6:9]] = [id]
                elif re.match(r'^owner = \w{1,99}', line):
                    owners[line[8:11]] = [id]
                elif re.match(r'^owner= \w{1,99}', line):
                    owners[line[7:10]] = [id]
                elif re.match(r'^owner =\w{1,99}', line):
                    owners[line[7:10]] = [id]

    #
    groupLines = []
    with open('Eu4/map/provincegroup.txt', 'r', encoding='utf-8') as pFile:
        groupLines.append(pFile.readlines())
        pFile.close()

    groups = {}
    ids=[]
    start = False
    for line in groupLines[0]:
        if not line.strip():
            continue
        if '{' in line:
            start = True
            ids=[]
            groupName = re.findall(r'^\w{1,99}', line)[0]
            if re.match(r'.*\d', line):
                ids.append(re.findall(r'\d{1,99}', line))
        elif start and not '}' in line:
            if re.match(r'.*\d', line):
                ids.append(re.findall(r'\d{1,99}', line))
        elif '}' in line:
            start = False
            if re.match(r'.*\d', line):
                ids.append(re.findall(r'\d{1,99}', line))
            groups[groupName] = ids

    return owners, groups