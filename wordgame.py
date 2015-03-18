#Laszlo Malina
#Wordgame Assignment
#14/11/2014


from flask import Flask, render_template, url_for, request, redirect, flash, session
from threading import Thread

import time
import random
import array
import itertools
import operator


app = Flask(__name__)

myresult=[False]*7
myresult2=[False]*7
count=1
wordsarray=[""]*7

#check words if its in the dictionary and if in source word then valid
#and if its a duplicate set to invalid
def checkvalidity(wordsarray):
    temp = [""]*7
    session['valid']=[""]*7
    
    for i in range(0,7):
        session['word'] = wordsarray[i]
        session['cwresult']= checkword(session['word'])# check word in dictionary
        session['ccresult']= checkchar(session['word'],session['source']) # check word in source word
    #print(ccresult)
        myresult[i]=session['cwresult']
        myresult2[i]=session['ccresult']
    #if both results are true the word is completely valid and not duplicates
        session['cdresult'] = checkduplicate(wordsarray)
        if session['cwresult'] and session['ccresult'] and session['cdresult']:
            temp[i]="Valid"
        else:
            temp[i]="Invalid"
    session['valid'] = temp
    
    return session['valid']

#check words against dictionary
def checkword(inLine):
    guesswords = [line.strip() for line in open('guesswords.txt')]
    for line in guesswords:
        if inLine.strip() in line.strip() and len(inLine.strip()) == len(line.strip()):
            return True
    return False

#check the word is in source words
def checkchar(string,source):
    sstring=sorted(string)
    ssource=sorted(source)
    for elem in sstring:
        if elem in ssource:
            ssource.remove(elem)
        else:
            return False
    return True

#check for a duplicate word
def checkduplicate(array):
    output = []
    duplicates=[]
    for x in array:
        if x not in output:
            output.append(x)
        else:
            duplicates.append(x)
    return duplicates

@app.route('/')
def home():
    return render_template("home.html",
                            the_title="The Word Game",
                            comment_url=url_for("getthewords"),
                            show_url=url_for("showthetop"))

@app.route('/play')
def getthewords():
    sourceword = [line.strip() for line in open('sourcewords.txt')]
    actualsource = random.choice(sourceword)
    session['source']=actualsource
    session['start'] = round(time.clock(),4)
    return render_template("enter.html",
                            the_title="Play the game",
                            the_save_url=url_for("enterwords"),
                            the_source=session.get('source'))

def check_log(a,b):
    with open('test.log', 'a') as log:
        print(a," was",b,file=log)

def storewords(one,two,three,four,five,six,seven):
    wordsarray=[""]*7

    wordsarray[0]=one
    wordsarray[1]=two
    wordsarray[2]=three
    wordsarray[3]=four
    wordsarray[4]=five
    wordsarray[5]=six
    wordsarray[6]=seven

    return wordsarray

def set_time(name,time):
    with open('board.log', 'a') as log:
        print(time,"___",name,file=log)
            
@app.route('/result', methods=["POST"])
def enterwords():
    all_ok = True

    session['thearray']=storewords(request.form['word_one'].lower(),request.form['word_two'].lower(),request.form['word_three'].lower(),request.form['word_four'].lower(),
    request.form['word_five'].lower(),request.form['word_six'].lower(),request.form['word_seven'].lower(),)
    session['result'] = checkvalidity(session['thearray'])
    if all_ok and session['cdresult']:
        session['finish']= round(time.clock(),4) - session['start']
        the_words=session.get('thearray')
        the_result=session.get('result')
        return render_template("invalid.html",the_title="Thanks for playing the game",
                            the_time=session.get('finish'),
                            the_words_results=zip(the_words,the_result),
                            home_link=url_for("home"))
        
    else:
        session['finish']= round(time.clock(),4) - session['start']
        
        return render_template("name.html",the_title="Just one more thing",
                            the_name_url=url_for("allvalid"),
                            home_link=url_for("home"))
        

@app.route('/allvalid',methods=["POST"])
def allvalid():
    set_time(request.form["player_name"],session['finish'])
    return render_template("valid.html",the_title="Thanks for playing the game!!",
                            the_player=request.form["player_name"],
                            the_time=session.get('finish'),
                            home_link=url_for("home"))
@app.route('/displaytop')
def showthetop():
    times=[""]*10
    names=[""]*10
    with open('board.log') as log:
        lines = log.readlines()
        lines.sort(key=lambda x:x[0])
        for i in range(0,10):
            sbs = lines[i].split('___')
            times[i] = sbs[0]
            names[i] = sbs[1]
    return render_template("show.html",
                            the_title="Top Scorers List",
                            the_data=zip(times,names),
                            home_link=url_for("home"))

app.config['SECRET_KEY'] = 'startrek'
if __name__ == '__main__':
	app.run(debug=True)
