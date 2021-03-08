from flask import Flask, render_template,url_for,flash, redirect
app = Flask(__name__)
from form2 import QueryForm, LoginForm, SelectionForm, CourseForm,DateForm,TaskForm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time 
import os
import getpass

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe" 
options = webdriver.ChromeOptions()
options.headless = True   
#options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=PATH)

app.config['SECRET_KEY']='f154e1e86eb3f11bba3ade756bf8d0'


course_dict={}
course_web={}
task_dict={}
task_web={}
upload_name={}

@app.route("/", methods=['GET','POST'])    
def registeration():
    form= QueryForm()
    if form.validate_on_submit():

     # if 'login' in '{form.query.data}':
        #print("hello")
        flash(f'OK! Provide login credentials{form.query.data}','success')  
        return redirect(url_for('login'))
     # else:
      #  flash(f'OK! Provide login credentials','success') 
    #else:
      #  flash(f'You need to login first to your account','danger')  
       # return redirect(url_for('login'))

    return render_template('query.html', title="SIGN UP", form=form)


@app.route("/login", methods=['GET','POST'])    
def login():

    form= LoginForm()
    driver.get("https://moodle.iitd.ac.in/login/index.php") 

    #username=input("Username: ")
    #password = getpass.getpass('Password:')
    username='{form.username.data}'
    password = '{form.password.data}'

    cap = driver.find_element_by_id("login").text
    st= cap[44:]
    words= st.split(' ') 

    user = driver.find_element_by_id("username")
    paswrd = driver.find_element_by_id("password")
    check=driver.find_element_by_id("rememberusername")
    btn=driver.find_element_by_id("loginbtn")
    capt=driver.find_element_by_id("valuepkg3") 
    user.send_keys(username) 

    temp = re.findall(r'\d+', st) 
    l = list(map(int, temp))
    do=0
    for i in words:
        if (i.isdigit()==True):
            continue
        elif(i=="add"):
            do=1
        elif(i=="subtract"):
            do=2
        elif(i=="first"):
            do=3
        elif (i=="second"):
            do=4
    out=l[0]

    if(do==1):
        out+=l[1]
    elif(do==2):
        out-=l[1]
    elif(do==4):
        out=l[1]
    capt.send_keys(Keys.BACKSPACE)
    capt.send_keys(out)
    check.click()
    paswrd.send_keys(password) 
    btn.click()

    if form.validate_on_submit():
        
        flash("""Provide details about the course!""", 'success')
        return redirect(url_for('course'))
        
    return render_template('login.html', title="SIGN In", form=form)

@app.route("/course_access", methods=['GET','POST'])    
def course():
    form= CourseForm()

            #driver.get('https://moodle.iitd.ac.in/course/index.php?categoryid=2')
            #courses=driver.find_elements_by_class_name('media-body')
            #print("You have successfully logged in!")
            #semester=input("Study Time! Your semester pls(eg. 2002)")
            #course=input("Specify course(eg. PYL101)>")
    semester='{form.sem.data}'
    course='{form.cour.data}'
    driver.get('https://moodle.iitd.ac.in/course/search.php?search='+semester+'%20'+course+'&perpage=all')
    results=driver.find_elements_by_xpath("//div[@class='info']/h3[@class='coursename']")
            
    course_dict2={}
    course_web2={}
    for i in range(1,len(results)+1):
               #print(i,':',results[i-1].text)
        course_dict2[i-1]=results[i-1].text
        web=results[i-1].find_element_by_tag_name('a')
        course_web2[i-1]=web.get_attribute('href')
    course_dict.update(course_dict2)
    course_web.update(course_web2)
    if form.validate_on_submit():
        flash("""We got your courses""", 'success')
        return redirect(url_for('select'))
        
    #return render_template('login.html', title="SIGN In", form=form)
    #except:
        #flash("""your login time out""", 'danger')
         #   return redirect(url_for('login'))
          
    return render_template('course_detail.html', title="SIGN In", form=form)

@app.route("/select_course", methods=['GET','POST'])    
def select():
    form= SelectionForm()

    #s=int(input('Type the course index from mentioned>'))
    y=form.ans.data
    s=int(y)    #print(course_web[s-1])
    website= course_web[s-1]
    driver.get(website)
    tas= driver.find_element_by_id("section-0")
    tasks=tas.find_elements_by_class_name('activityinstance')
    #task_dict={}
    #task_web={}
    for j in range(1,len(tasks)+1):
                #print(j,':',tasks[j-1].text)
                task_dict[j-1]=tasks[j-1].text
                web_task=tasks[j-1].find_element_by_tag_name('a')
                task_web[j-1]=web_task.get_attribute('href')
            #print(len(task_dict)+1,':',"UPLOADS")
    task_dict[len(task_dict)]="UPLOADS"
    if form.validate_on_submit():
        
        flash(f'I got your course !','success')  
        return redirect(url_for('task'))
    return render_template('course_select.html', title="SIGN UP", form=form)

@app.route("/select_task", methods=['GET','POST'])
def task():
    form= TaskForm()
            
    t='{form.task.data}'
    #t=int(input('Type the task index from mentioned>'))
    #print(len(task_web))
    #print(len(task_dict))
    if(t!=len(task_web)+1):
        driver.get(task_web[t-1])
        try:
            test=driver.find_element_by_xpath("//*[@id='region-main']/div[1]/table/thead/tr/th[1]")
            row=len(driver.find_elements_by_xpath("//*[@id='region-main']/div[1]/table/tbody/tr"))
            column=len(driver.find_elements_by_xpath("//*[@id='region-main']/div[1]/table/tbody/tr[1]/td"))
            head=driver.find_elements_by_xpath("//*[@id='region-main']/div[1]/table/thead/tr/th")
            a="//*[@id='region-main']/div[1]/table/thead/tr/th["
            for x in range(1,len(head)+1):
                full=a+str(x)+"]"
                print(driver.find_element_by_xpath(full).text,end=" ")
            b="//*[@id='region-main']/div[1]/table/tbody/tr["
            e=']/td['
            for i in range(1,row+1):
                c=str(i)
                for j in range (1,column+1):
                    full2=b+c+e+str(j)+']'
                    #print(driver.find_element_by_xpath(full2).text,end=' ')
        except:
            pass      
                  #driver2.get(task_web[t-1])
                  #("Your required task is done, there is nothing to show")
    else:
        flash(f'You need to specify date !','success')  
        return redirect(url_for('date'))
    return render_template('task_select.html', title="SIGN UP", form=form)
@app.route("/select_date", methods=['GET','POST'])
def date():
                form= DateForm()
                d=int('{form.date.data}')
                #int(input('Specify date to get uploads(01-31)>'))
                mon='{form.mon.date}'
                #driver.get(task_web[t-1])
                #input('Specify Month (eg. February)>')
                upload_date=driver.find_elements_by_class_name("sectionname")
                up_doc=driver.find_elements_by_class_name('content')
        
                ind=4
                z=2
                for k in range(1,len(up_doc)+1):

                  if ((mon in upload_date[ind-1].text)and((d<=int(upload_date[ind-1].text[:1]))or(d>=int(upload_date[ind-1].text.split('-')[1][1:2])))):
                    try:
                      doc=up_doc[z-1].find_elements_by_class_name("activityinstance")
                      for l in range(0,len(doc)):
                        upload_name[l]=doc(l)
                        #print(l.text)
                      flash(f'We got you uploads !','success')  
                      return redirect(url_for('uploads'))
                    except:
                      flash(f'No uploads for provided date !','success')  
                      return redirect(url_for('uploads_got'))
                      
                    break
                  ind+=2
                  z+=1 
                return render_template('date_in.html', title="SIGN UP", form=form)
@app.route("/upload_for")
def uploads_got():
        return render_template('uploads.html', upload_name = upload_name , title="HOME")
if __name__=="__main__":
    app.run(debug = True, host="127.0.0.1", port=8080, threaded=True)
