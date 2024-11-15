from flask import Flask, render_template, request, redirect, flash, url_for, session
import MySQLdb
import time
import subprocess
import os

#

import re
import PyPDF2
# Required Libraries
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download resources for nltk (if not already done)
nltk.download('punkt')
nltk.download('stopwords')

#

app = Flask (__name__)
app.secret_key = "secret key"

@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html')


# Admin Login
@app.route("/adminlogin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        uid=request.form["uid"]
        pwd=request.form["pwd"]

        if uid=="Admin" and pwd=="Admin":
            return render_template("adminhome.html")
        else:
            return render_template("adminlogin.html", msg="Your Login attempt was not successful. Please try again!!")
    return render_template("adminlogin.html")

#Admin Upload Question Details
@app.route("/adminaddquestiondetails", methods=["GET", "POST"])
def admin_addlquestiondetails():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()

    if request.method == "POST" :
        if request.form["b1"] == "Upload":
           c1.execute("select ifnull(max(fid),0)+1 from questable")
           row = c1.fetchone()
           fid = int(row[0])
           dname=request.form["dname"]
           cyear = request.form["cyear"]
           subname = request.form["subname"]
           c1.execute("select * from questable where dname='%s' and cyear='%s' and subname='%s'" % (dname,cyear,subname))
           row = c1.fetchone()

           if (row is not None):
               return render_template("adminaddquestiondetails.html", msg="Question Upload Details Already Inserted")


           f1 = request.files['qfile']
           f1.save(os.getcwd() + "\\static\\question\\" + f1.filename)
           qfile = f1.filename

           f2 = request.files['afile']
           f2.save(os.getcwd() + "\\static\\answer\\" + f2.filename)
           afile = f2.filename


           c1.execute("insert into questable values(%d,'%s','%s','%s','%s','%s')"%(fid,dname,cyear,subname,qfile,afile))
           db.commit()
           return render_template("adminaddquestiondetails.html", msg="Question Upload Details Successfully Inserted")

    return render_template("adminaddquestiondetails.html", msg="")

# Admin View Question Details
@app.route("/adminviewquestiondetails", methods=["GET", "POST"])
def admin_viewjobdetails():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    c1.execute("select * from questable")
    data = c1.fetchall()
    return render_template("adminviewquestiondetails.html", data=data)


#Admin Delete Question Details
@app.route("/admindeletequestiondetails/<int:fid>", methods=["GET", "POST"])
def admin_deletequestiondetails(fid):
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()

    c1.execute("Select qfile,afile from questable where fid='%d'" %(fid))
    d=c1.fetchone()
    fname1=""
    fname2=""
    if (d is not None):
        fname1=str(d[0])
        fname2 =str(d[1])
        c1.execute("delete from questable where  fid='%d'" %(fid))
        db.commit()
        fname=os.getcwd() + "\\static\\question\\" + fname1
        if (os.path.isfile(fname)):
            os.remove(fname)

        fname = os.getcwd() + "\\static\\answer\\" + fname2
        if (os.path.isfile(fname)):
            os.remove(fname)

    c1.execute("select * from questable")
    row = c1.fetchall()
    return render_template("adminviewquestiondetails.html", data=row, msg="")


#New student Registration
@app.route("/studentregistration", methods=["GET", "POST"])
def student_registration():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()

    if request.method == "POST" :
        if request.form["b1"] == "Register":
            emailid = request.form["emailid"]
            c1.execute("select * from studtable where emailid='%s'" % emailid)
            row = c1.fetchone()
            if (row is not None):
                return render_template("studentregistration.html", msg="EmailId Already Found!!")

            sname = request.form["sname"]
            gender = request.form["gender"]
            cname = request.form["cname"]
            dname=request.form["dname"]
            cyear = request.form["cyear"]
            mno = request.form["mno"]
            pword = request.form["pword"]

            c1.execute("insert into studtable values('%s','%s','%s','%s','%s','%s','%s','%s')" %(sname, gender, cname, dname, cyear,emailid,mno,pword))
            db.commit()

            return render_template("studentregistration.html", msg="Registration Details Inserted!!!")

    return render_template("studentregistration.html", msg="")


# Admin View Student
@app.route("/adminviewstudent")
def admin_viewstudent():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    c1.execute("select * from studtable")
    data = c1.fetchall()
    return render_template("adminviewstudent.html", data=data)


# student Login
@app.route("/studentlogin", methods=["GET","POST"])
def studentlogin():
    if request.method == "POST":
        db = MySQLdb.connect("localhost", "root", "", "ocrdb")
        c1 = db.cursor()
        emailid=request.form["emailid"]
        pword=request.form["pword"]

        c1.execute("select * from studtable where emailid='%s' and pword='%s'"%(emailid,pword))
        if c1.rowcount>=1:
            row=c1.fetchone()
            sname=row[0]
            dname=row[3]
            cyear=row[4]
            session["emailid"]=emailid
            session["studname"]=sname
            session["deptname"]=dname
            session["cyear"]=cyear
            return render_template("studenthome.html", msg="")
        else:
            return render_template("studentlogin.html", msg="Your Login attempt was not successful. Please try again!!")

    return render_template("studentlogin.html")

#Student View Profile
@app.route("/studentviewprofile")
def student_viewprofile():
    db=MySQLdb.connect("localhost","root","","ocrdb")
    c1 = db.cursor()
    emailid=session["emailid"]

    c1.execute("select * from studtable where emailid='%s'"%emailid)
    if c1!=None:
        row=c1.fetchall()

        return render_template("studentviewprofile.html", data=row)

#student View question
@app.route("/studentviewquestion")
def student_viewquestion():
    db=MySQLdb.connect("localhost","root","","ocrdb")
    c1 = db.cursor()
    sname=session["studname"]
    emailid=session["emailid"]
    dname=session["deptname"]
    cyear=session["cyear"]

    c1.execute("select * from questable where dname='%s' and cyear='%s'"%(dname, cyear))
    if c1!=None:
        row=c1.fetchall()

        return render_template("studentviewquestion.html", sname=sname,emailid=emailid,dname=dname,cyear=cyear,data=row)


#student answer upload
@app.route("/studentanswerupload")
def student_answerupload():
    db=MySQLdb.connect("localhost","root","","ocrdb")
    c1 = db.cursor()
    sname=session["studname"]
    emailid=session["emailid"]
    dname=session["deptname"]
    cyear=session["cyear"]

    c1.execute("select * from questable where dname='%s' and cyear='%s' and subname not in (select subname from answerupload where emailid='%s' and dname='%s' and cyear='%s')"%(dname, cyear,emailid,dname,cyear))
    if c1!=None:
        row=c1.fetchall()

        return render_template("studentanswerupload.html", sname=sname,emailid=emailid,dname=dname,cyear=cyear,data=row)


#Student Answer Upload1
@app.route("/studentuploadanswer1/<subname>", methods=["GET", "POST"])
def student_uploadanswer1(subname):
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    sname = session["studname"]
    emailid = session["emailid"]
    dname = session["deptname"]
    cyear = session["cyear"]
    return render_template("studentuploadanswer.html", sname=sname, emailid=emailid, dname=dname, cyear=cyear,subname=subname)


#Student Upload Answer Details
@app.route("/studentuploadanswer", methods=["GET", "POST"])
def student_uploadanswer():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    if request.method == "POST" :
        if request.form["b1"] == "Upload":
           c1.execute("select ifnull(max(auid),0)+1 from answerupload")
           row = c1.fetchone()
           auid = int(row[0])
           sname = session["studname"]
           emailid = session["emailid"]
           dname = session["deptname"]
           cyear = session["cyear"]
           subname = request.form["subname"]


           c1.execute("select * from answerupload where emailid='%s' and dname='%s' and cyear='%s' and subname='%s'" % (emailid,dname,cyear,subname))
           row = c1.fetchone()

           if (row is not None):
               return render_template("studentuploadanswer.html", msg="Answersheet Upload Details Already Inserted", sname=sname, emailid=emailid, dname=dname, cyear=cyear,subname=subname)


           f1 = request.files['afile']
           f1.save(os.getcwd() + "\\static\\StudentAnswer\\" + f1.filename)
           safile = f1.filename
           t = time.localtime()
           s = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday)
           audate = s

           c1.execute("insert into answerupload values(%d,'%s','%s','%s','%s','%s','%s','%s')"%(auid,sname,emailid,dname,cyear,subname,safile,audate))
           db.commit()
           return render_template("studentuploadanswer.html", msg="Student Answer Upload Details Successfully Inserted", sname=sname, emailid=emailid, dname=dname, cyear=cyear,subname=subname)






# Admin View Answersheet Upload Details
@app.route("/adminscoreevaluation", methods=["GET", "POST"])
def admin_scoreevaluation():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    c1.execute("select * from answerupload where auid not in (select auid from resulttable)")
    data = c1.fetchall()
    return render_template("adminscoreevaluation.html", data=data)


#Admin Score Evaluation
@app.route("/adminscoreevaluation1/<int:auid>", methods=["GET", "POST"])
def admin_scoreevaluation1(auid):
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    c1.execute("select * from answerupload where auid='%d'" %(auid))
    row = c1.fetchone()
    if(row is not None):
        auid = int(row[0])
        sname = row[1]
        emailid = row[2]
        dname=row[3]
        cyear=row[4]
        subname = row[5]
        asheet = row[6]
        return render_template("adminscoreevaluation1.html", auid=auid,sname=sname, emailid=emailid,dname=dname,cyear=cyear, subname=subname,asheet=asheet)


#

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        pdf_file.close()

        #print(text)

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    txt_file.close ();



def s_pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        pdf_file.close ()
    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    txt_file.close ()


def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())

    # Remove Stopwords and Non-alphabetical tokens
    tokens = [word for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(tokens)


# Cosine Similarity Function
def calculate_similarity(text1, text2):
    # Use TfidfVectorizer to convert texts to numerical format
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Compute Cosine Similarity between two texts
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity[0][0]


# Descriptive Answer Evaluation Function
def evaluate_answer(model_answer, student_answer):
    # Preprocess the model and student answers
    model_answer_processed = preprocess_text(model_answer)
    student_answer_processed = preprocess_text(student_answer)

    # Calculate similarity score
    similarity_score = calculate_similarity(model_answer_processed, student_answer_processed)

    # Scoring system based on similarity (can be customized)
    if similarity_score >= 0.8:
        grade = 'A'
    elif similarity_score >= 0.6:
        grade = 'B'
    elif similarity_score >= 0.4:
        grade = 'C'
    else:
        grade = 'D'

    return {
        'similarity_score': similarity_score,
        'grade': grade
    }


def split_paragraphs_from_file(oa_file_path1,sa_file_path1):
    try:
        with open(oa_file_path1, 'r') as file:
            content = file.read()

        file.close ()
        data = re.split(r"\b\d+\.\s+", content.strip())

        oanswer=[]
        for x in data :
            if(len(x)!=0):
                x=x.strip()
                oanswer.append(x)


        sanswer=[]

        with open(sa_file_path1, 'r') as file:
            content = file.read()

        file.close ()
        data = re.split(r"\d+\.\s+", content.strip())

        sanswer = []
        for x in data:
            if(len(x)!=0):
                x = x.strip()
                sanswer.append(x)



        totalanswer =len(oanswer)
        studentanswer=len(sanswer)
        calculateanswer=0

        if (totalanswer>studentanswer):
            calculateanswer =studentanswer
        elif(totalanswer<studentanswer):
            calculateanswer=totalanswer
        else :
            calculateanswer=totalanswer

        sscore = 0
        for i in range(calculateanswer):
            model_answer = oanswer[i]
            student_answer = sanswer[i]
            result = evaluate_answer(model_answer, student_answer)
            # print("Similarity Score:", result['similarity_score'])
            sscore = sscore + float(result['similarity_score'])

        fscore = round(sscore / len(sanswer), 2)
        #print("Final Score :", fscore)
        if fscore >= 0.8:
            grade = 'A'
        elif fscore >= 0.6:
            grade = 'B'
        elif fscore >= 0.4:
            grade = 'C'
        else:
            grade = 'D'

        #print("Grade :", grade)




    except Exception as e:
        print(f"An error occurred: {e}")

    return {
        'Similarity_Score': fscore,
        'Grade': grade
         }


#



#Admin Score Evaluation
@app.route("/adminscoreevaluation2", methods=["GET", "POST"])
def admin_scoreevaluation2():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    if request.method == "POST" :
        if request.form["b1"] == "Upload":
            auid = int(request.form["auid"])
            sname=request.form["sname"]
            emailid = request.form["emailid"]
            dname=request.form["dname"]
            cyear=request.form["cyear"]
            subname=request.form["subname"]
            asheet=request.form["asheet"]
            c1.execute("select * from questable where dname='%s' and cyear='%s' and subname='%s'" % (dname, cyear,subname))
            row = c1.fetchone()
            oasheet=row[5]
            # os.getcwd() + "\\static\\answer\\" + f2.filename
            pdf_path = os.getcwd() + "\\static\\answer\\" +oasheet
            txtfile=oasheet[0:oasheet.index(".pdf")]
            txtfile =txtfile +".txt"
            output_txt = os.getcwd() + "\\static\\AdminUploadFile\\AdminUploadFile1\\"+ txtfile
            pdf_to_text(pdf_path, output_txt)

            pdf_path1 = os.getcwd() + "\\static\\AdminUploadFile\\AdminUploadFile1\\Verification\\"+asheet
            txtfile1 = asheet[0:asheet.index(".pdf")]
            txtfile1 = txtfile1 + ".txt"
            output_txt1 = os.getcwd() + "\\static\\StudentAnswerSheet\\StudentAnswerSheet1\\"+txtfile1
            s_pdf_to_text(pdf_path1, output_txt1)

            d=split_paragraphs_from_file(output_txt,output_txt1 )
            #print("Subject Name :", subname,"\nScore :", d['Similarity_Score'],"\nGrade :", d["Grade"])
            per=float(d['Similarity_Score'])*100
            grade=d["Grade"]
            c1.execute("select * from resulttable where auid='%d'" %(auid))
            row = c1.fetchone()

            if (row is not None):
                return render_template("adminscoreevaluation1.html", msg="Score Evaluation Details Already Inserted", auid=auid,sname=sname,emailid=emailid, dname=dname, cyear=cyear, subname=subname,asheet=asheet)

            c1.execute("insert into resulttable values(%d,'%s','%s','%s','%s','%s','%f','%s')" % (auid, sname, emailid, dname, cyear, subname, per, grade))
            db.commit()
            return render_template("adminscoreevaluation1.html", msg="Score Evaluation Details Successfully Inserted", auid=auid,sname=sname, emailid=emailid, dname=dname, cyear=cyear, subname=subname, asheet=asheet)

# Admin View Result
@app.route("/adminviewresult")
def admin_viewresult():
    db = MySQLdb.connect("localhost", "root", "", "ocrdb")
    c1 = db.cursor()
    c1.execute("select * from resulttable")
    data = c1.fetchall()
    return render_template("adminviewresult.html", data=data)

#student View result
@app.route("/studentviewresult")
def student_viewresult():
    db=MySQLdb.connect("localhost","root","","ocrdb")
    c1 = db.cursor()
    sname=session["studname"]
    emailid=session["emailid"]
    dname=session["deptname"]
    cyear=session["cyear"]

    c1.execute("select * from resulttable where emailid='%s' and dname='%s' and cyear='%s'"%(emailid,dname, cyear))
    if c1!=None:
        row=c1.fetchall()

        return render_template("studentviewresult.html", sname=sname,emailid=emailid,dname=dname,cyear=cyear,data=row)


@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run (debug=True)