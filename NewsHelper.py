import requests
from bs4 import BeautifulSoup
from tkinter import *
import urllib.request
from urllib.request import urlopen
from urllib.parse import quote_plus


def alert():
    print("Task Start")
    
    # DATA
    url_base = "http://www.teentimes.org/newspapers/view/"

    # *** request login
    session = requests.session()
    url = "http://www.teentimes.org/auths/login"


    data = {
        "_method" : "POST",
        "data[Member][MEMBER_ID]" : ID_Entry.get(),
        "data[Member][PASSWD]" : PW_Entry.get(),
        "data[Member][login_check]" : "1"
    }


    response = session.post(url, data= data)

    response.raise_for_status()


    for x in range(0, int(NB_Entry.get())):
        # calculate URL
        url_numb = int(URL_Entry.get())

        urlStr = []
        urlStr.append(url_base)
        urlStr.append(str(url_numb + x))
        url = ''.join(urlStr)

        # *** scrap article

        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")


        # get title
        title = soup.select("h6")[0].get_text()
        print(title[1:])

        # get article
        mainArticle = soup.select(".eng")

        # get translated title
        translated = soup.select(".s_area_trans")[0].get_text().split('\n')

        for x in range(len(translated)):
            translated[x] = translated[x].replace("	","").replace("\r","")

        translatedTitle = translated[1]

        translated.remove(translated[0])
        translated.remove(translatedTitle)



        # get voca
        vocaEng = soup.select(".s_word_eng")
        vocaKor = soup.select(".s_word_kor")


            
        # get translated article

        tempSentence = ""
        for sentence in translated:
            if sentence != "" :
                tempStr = []
                tempStr.append(tempSentence)
                tempStr.append(sentence)
                tempSentence = ' '.join(tempStr)
            
            else :
                tempStr = []
                tempStr.append(tempSentence)
                tempStr.append('\n')
                tempSentence = ' '.join(tempStr)
                
        translatedArticle = tempSentence.split('\n')

        # get img
        imgurlHTML = [];
        imgurlStr = [];
        
        imgurlHTML = soup.select(".s_newsimg_over")
        try :
            imgurlStr = str(imgurlHTML[0]).split('"')
            imgurl = imgurlStr[5]

            with urlopen(imgurl) as f:
                with open(title[1:] + '.jpg','wb') as h: # w - write b - binary
                    img = f.read()
                    h.write(img)

       
        except :
            print("error - no image found")

        
        # write file
        fileNameStr = []
        fileNameStr.append(title[1:])
        fileNameStr.append(".txt")
        fileName = ''.join(fileNameStr)

        file = open(fileName, 'w')

        file.write(title[1:])
        file.write('\n')
        file.write('\n')


        for paragraph in mainArticle:
           file.write(paragraph.get_text())
           file.write('\n')
        file.write('\n')
        file.write('\n')


        file.write(translatedTitle)
        file.write('\n')
        file.write('\n')

        for index in range(len(vocaEng)):
            file.write(vocaEng[index].get_text() + '\t' + vocaKor[index].get_text())
            file.write('\n')
        file.write('\n')
        file.write('\n')

        for translatedSentence in translatedArticle:
            file.write(translatedSentence[1:])
            file.write('\n')

        file.close()

    print("Task Done")


# UI 구성

win = Tk()

    
win.geometry("600x300")
win.title("CNE news")
win.option_add("*Font", "맑은고딕 15")

ID_Label = Label(win, text = "   ID : ")
ID_Entry = Entry(win)

PW_Label = Label(win, text = "   PW : ")
PW_Entry = Entry(win)

URL_Label = Label(win, text = "   파일 작성을 시작할 news의 번호 : ")
URL_Entry = Entry(win)

NB_Label = Label(win, text = "   연속 몇 개의 글을 작성할까요 : ")
NB_Entry = Entry(win)

    
btn = Button(win, text="만들기")
btn.config(command = alert, width = 30, height = 3)


ID_Label.grid(row = 0, column = 0, sticky = "e")
ID_Entry.grid(row = 0, column = 1)

PW_Label.grid(row = 1, column = 0, sticky = "e")
PW_Entry.grid(row = 1, column = 1)

URL_Label.grid(row = 3, column = 0, sticky = "e")
URL_Entry.grid(row = 3, column = 1)

NB_Label.grid(row = 4, column = 0, sticky = "e")
NB_Entry.grid(row = 4, column = 1)

btn.grid(row = 5, column = 0, columnspan = 2)

win.mainloop()





