#Imports
from tools import *
from glob import glob
import numpy as np

def main():
    #Open Files
    baseHtmlsFiles = glob('htmls/baseFiles/*.html')
    htmls = {parseHtmls(i)[0][5:][:len(parseHtmls(i)[0])-10]:parseHtmls(i) for i in baseHtmlsFiles}

    #Get Eu4 Info
    owners, groups = parseEu4()

    #Get tags by region:
    tagGroups = {}
    for gKey in groups:
        tags=[]
        for oKey in owners:
            for gLists in groups[gKey]:
                for gList in gLists:
                    for id in gList:
                        if id in owners[oKey]:
                            if not oKey in tags:
                                tags.append(oKey)
        tagGroups[gKey]=tags

    print(tagGroups)

    #Change Files
    #Regions.html
    regions = htmls['regions.html']
    for key in tagGroups:
        if len(tagGroups[key])>0:
            if len(tagGroups[key])>1:
                regions.insert(26, tagGroups[key][0]+'<br><br>\n')
                if len(tagGroups[key])>2:
                    for tag in tagGroups[key][1:len(tagGroups[key])-1]:
                        regions.insert(26, tag+' ')
                regions.insert(26, '\t\t\t'+tagGroups[key][len(tagGroups[key])-1]+'<div class="tab"></div>')
            else:
                regions.insert(26, '\t\t\t'+tagGroups[key][0]+'<br><br>\n')
            regions.insert(26, '\t\t\t'+f'<a href=\"tags\{key}.html\">{key}</a>'+'<br><br>\n')

    existingGroupFiles = glob('htmls/tags/*.html')
    testHtml = parseHtmls(r'htmls\baseFiles\others\test.html')
    for key in tagGroups:
        if not f'htmls/tags/{key}.html' in existingGroupFiles:
            keyHtml = open(f'htmls/tags/{key}.html', 'w+', encoding='utf-8')
            for line in testHtml:
                keyHtml.write(line)
            keyHtml.close()


    htmlsFiles=glob('htmls/*.html')
    #Save files
    saveHtmls(htmls, htmlsFiles)
    

if __name__ == '__main__':
    main()