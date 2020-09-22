import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []
        
    def DownloadData(self,searchTerm,NoOfTerms):       
        self.searchTerm=searchTerm
        self.NoOfTerms=NoOfTerms

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
        j=1

        # creating frames, text "TWEETS: " & button "SEE GENERAL REPORT"
        Frame1=Frame(frame2,bg="lightblue",width=500)
        Frame1.grid(pady=2,row=1,sticky=W+E)
    
        Frame2=Frame(frame2,relief="raised",width=500)
        Frame2.grid(pady=2,row=2,sticky=W+E)
        
        m1 = Message(Frame1,text=" SOME TWEETS:",font="Helvetia 11 bold italic",justify=CENTER,width=500,relief="solid")
        m1.pack(fill=X,anchor="n",side="left",pady=2)

        b3=Button(Frame1,text="SEE GENERAL REPORT >>",command=lambda: self.del2(Frame1,Frame2,positive,negative,neutral,polarity),
                  font="Times 9 ",relief='raised',cursor="hand2")
        b3.pack(anchor="n",pady=2,padx=2,side="right")

        b2=Button(Frame1,text="<< BACK",command=lambda: self.back1(Frame1,Frame2),font="Times 9 ",relief='raised',cursor="hand2")
        b2.pack(anchor='n',side="right",pady=2, padx=2)

        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. Using encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)

            if j<=7:
                m=Message(Frame2,text="%s\n\nPOLARITY = %s , SUBJECTIVITY = %s"%(tweet.text.translate(non_bmp_map),analysis.sentiment.polarity,analysis.sentiment.subjectivity),
                      justify=CENTER,width=500,relief='solid') #print tweet's text
                m.pack(fill=X,anchor='n',side="top",pady=2)
                j+=1
                u=tweet.text
                u=u.encode('unicode-escape').decode('utf-8')    
            
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0):
                positive += 1
            else:
                negative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms


    def gen_report(self,positive,negative,neutral,polarity,Frame1,Frame2):
        pol=""
        frame1.config(bg="SystemButtonFace")
        caption2.config(bg="SystemButtonFace")

        Frame3=Frame(frame2,relief="raised",bg="lightblue",width=500)
        Frame3.grid(padx=2,pady=2,row=1,sticky=W+E)
        
        m2=Message(Frame3,text="\nHow people are reacting on '%s' by analyzing %s tweets :\n"%(self.searchTerm,str(self.NoOfTerms)), bg="white",
                  justify=CENTER,width=500,relief='solid',font ="Helvetica 12 bold")
        m2.pack(fill=X,anchor='n',side="top",pady=12,padx=2,expand=10)
            
        if (polarity == 0):
            pol="Neutral"
        elif (polarity > 0 and polarity <= 1):
            pol="Positive"
        else:
            pol="Negative"

        m3=Message(Frame3,text="GENERAL REPORT :\n%s "%(pol), font ="Helvetica 10 bold",justify=CENTER,width=500,relief='solid',bg="white")
        m3.pack(fill=X,anchor='n',side="top",pady=10,padx=2,expand=2)

        m4=Message(Frame3,text="DETAILED REPORT :\n%s %% people thought it was positive.\n%s %% people thought it was negative.\n%s %% people thought it was neutral."%(positive,negative,neutral),                      
                       font ="Helvetica 10 bold",justify=CENTER,width=500,relief='solid',bg="white")
        m4.pack(fill=X,anchor='n',side="top",pady=10,padx=2,expand=2)

        b4=Button(Frame3,text="EXIT >>",command=master.destroy,font="Times 11 bold",relief='raised',height=1,cursor="hand2",bg="white",justify=CENTER)
        b4.pack(anchor='e',side="right",pady=16, padx=5)

        b5=Button(Frame3,text="VIEW GRAPHICAL RESULT >>",command=lambda: self.plotPieChart(positive,negative,neutral),
                  font="Times 11 bold",relief='raised',height=1,cursor="hand2",bg="white",justify=CENTER)
        b5.pack(anchor='e',side="right",pady=16, padx=8)

        b6=Button(Frame3,text="<< BACK",command=lambda: self.back2(Frame1,Frame2,Frame3),font="Times 11 bold",relief='raised',height=1,cursor="hand2",bg="white",justify=CENTER)
        b6.pack(anchor='w',side="left",pady=16, padx=5)
            

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive,negative,neutral):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive,neutral, negative]
        colors = ['darkgreen', 'gold','red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on "' + self.searchTerm + '" by analyzing ' + str(self.NoOfTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def del1(self):
        searchTerm = e1.get()
        NoOfTerms = int(e2.get())
        grids1=[l1,l2,e1,e2,b1]
        for i in grids1:
            i.grid_forget()
        self.DownloadData(searchTerm,NoOfTerms)

    def del2(self,Frame1,Frame2,positive,negative,neutral,polarity):
        Frame1.grid_forget()
        Frame2.grid_forget()
        self.gen_report(positive,negative,neutral,polarity,Frame1,Frame2)

    def back1(self,Frame1,Frame2):
        Frame1.grid_forget()
        Frame2.grid_forget()
        l1.grid(row=0,column=0,pady=10,sticky=W+E)
        e1.grid(row=0,column=1,sticky=W+E)
        l2.grid(row=1,column=0,pady=8,sticky=W+E)
        e2.grid(row=1,column=1,sticky=W+E)
        b1.grid(row=4,padx=5,pady=5,column=1)
        
            
    def back2(self,Frame1,Frame2,Frame3):
        Frame3.grid_forget()
        Frame1.grid(pady=2,row=1,sticky=W+E)
        Frame2.grid(pady=2,row=2,sticky=W+E)
        


sa = SentimentAnalysis()
# authenticating
consumerKey = 'tZLjnEW3QbBYODXgQGUe0w28i'
consumerSecret = 'kZ4UpJWs5y98fmWwO45PhnYkY6LjRcG8p5MYn3Uham3UCvDbMb'
accessToken = '86694879-O8iuOLloI42O88joeV7YI9yaV5q3Z0vury4CnwWXh'
accessTokenSecret = 'zXWtRULyRKsig8CYcvK0xlivdPbfcYtvn9dSxNqU21G1h'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

master=Tk()
master.title("Welcome!")
master.config(bg='lightblue')
master.geometry('500x600')

#CAPTION TWITTER LOGO
frame1=Frame(master,borderwidth=2,relief='solid',bg='white')
frame1.pack(padx=2,fill=X,side="top")

logo = PhotoImage(file="bird2.png")

caption1= Label(frame1, image=logo,bg='white')
caption1.pack(side="left",padx=20)

caption2=Label(frame1,text="TWITTER SENTIMENT ANALYSIS",bg='white',font="Verdana 15 bold italic")
caption2.pack(fill=BOTH,padx=5,side="left")

#ENTRY FIELDS
frame2=Frame(master,relief='ridge',bg='lightblue')
frame2.pack(fill=BOTH,side="top")

l1=Label(frame2,text="Enter Keyword/Tag to search about: ",font="Times 13",relief="groove")
l1.grid(row=0,column=0,pady=10,sticky=W+E)
e1=Entry(frame2,width=38,relief='solid')
e1.grid(row=0,column=1,sticky=W+E)

l2=Label(frame2,text="Enter how many tweets to analyze: ",font="Times 13",relief='groove')
l2.grid(row=1,column=0,pady=8,sticky=W+E)
e2=Entry(frame2,relief='solid')
e2.grid(row=1,column=1,sticky=W+E)

b1=Button(frame2,text="Search Tweets >>",command=sa.del1,font="Times 11 bold",relief='raised',height=1,cursor="hand2")
b1.grid(row=4,padx=5,pady=5,column=1)
    
mainloop()
    
