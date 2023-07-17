from typing import DefaultDict
import win32com.client as win32
import glob

debug = False

docProp = DefaultDict(list)
docProp["wdPropertyAppName"]= [	9,	"Name Of Application"]
docProp["wdPropertyAuthor"]= [	3,	"Author"]
docProp["wdPropertyBytes"]= [	22,	"Byte Count"]
docProp["wdPropertyCategory"]= [	18,	"Category"]
docProp["wdPropertyCharacters"]= [	16,	"Character Count"]
docProp["wdPropertyCharsWSpaces"]= [	30,	"Character Count With Spaces"]
docProp["wdPropertyComments"]= [	5,	"Comments"]
docProp["wdPropertyCompany"]= [	21,	"Company"]
docProp["wdPropertyKeywords"]= [	4,	"Keywords"]
docProp["wdPropertyLastAuthor"]= [	7,	"Last Author"]
docProp["wdPropertyLines"]= [	23,	"Line Count"]
docProp["wdPropertyManager"]= [	20,	"Manager"]
docProp["wdPropertyNotes"]= [	26,	"Notes"]
docProp["wdPropertyPages"]= [	14,	"Page Count"]
docProp["wdPropertyParas"]= [	24,	"Paragraph Count"]
docProp["wdPropertyRevision"]= [	8,	"Revision Number"]
docProp["wdPropertySecurity"]= [	17,	"Security Setting"]
docProp["wdPropertySubject"]= [	2,	"Subject"]
docProp["wdPropertyTemplate"]= [	6,	"Template Name"]
docProp["wdPropertyTimeCreated"]= [	11,	"Time Created"]
docProp["wdPropertyTimeLastPrinted"]= [	10,	"Time Last Printed"]
docProp["wdPropertyTimeLastSaved"]= [	12,	"Time Last Saved"]
docProp["wdPropertyTitle"]= [	1,	"Title"]
docProp["wdPropertyVBATotalEdit"]= [	13,	"Number Of Edits To VBA Project"]
docProp["wdPropertyWords"]= [	15,	"Word Count"]


word = win32.Dispatch("Word.Application")
if debug: word.Visible = 1
pathname = r'PUT_PATHNAME_HERE'
paths = glob.glob(pathname=pathname,recursive=True)
for file in paths:
    print(file)
    doc = word.Documents.Open(file)
    try:     
        for x in docProp.keys():
            prop = docProp[x][0]
            #print(prop)
            try:
                y = doc.BuiltInDocumentProperties(prop)
                print(y.Name, "  :  ", y.Value)
            except Exception as x:
                print(x)

    except Exception as e:
        print ('\n\n', e)
        doc.Close(0)
        continue
    doc.Close(0)
word.Quit()
