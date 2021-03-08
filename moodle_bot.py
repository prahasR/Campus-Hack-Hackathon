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
driver = webdriver.Chrome(executable_path=PATH,options=options)
#driver2=webdriver.Chrome(PATH)
#f=open("training_data/personal_ques.txt","a")
query=input('Hello! I am a moodle bot! what you want me to do?')

if 'login' in query:
    driver.get("https://moodle.iitd.ac.in/login/index.php") 

    username=input("Username: ")
    password = getpass.getpass('Password:')

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

    log=1
    while(log==1):
        try:
            driver.get('https://moodle.iitd.ac.in/course/index.php?categoryid=2')
            courses=driver.find_elements_by_class_name('media-body')
            print("You have successfully logged in!")
            semester=input("Study Time! Your semester pls(eg. 2002)")
            course=input("Specify course(eg. PYL101)>")
            driver.get('https://moodle.iitd.ac.in/course/search.php?search='+semester+'%20'+course+'&perpage=all')
            results=driver.find_elements_by_xpath("//div[@class='info']/h3[@class='coursename']")
            website=''
            course_dict={}
            course_web={}
            for i in range(1,len(results)+1):
               print(i,':',results[i-1].text)
               course_dict[i-1]=results[i-1].text
               web=results[i-1].find_element_by_tag_name('a')
               course_web[i-1]=web.get_attribute('href')
            s=int(input('Type the course index from mentioned>'))
    #print(course_web[s-1])
            website+=course_web[s-1]
            driver.get(website)
            tas= driver.find_element_by_id("section-0")
            tasks=tas.find_elements_by_class_name('activityinstance')
            task_dict={}
            task_web={}
            for j in range(1,len(tasks)+1):
                print(j,':',tasks[j-1].text)
                task_dict[j-1]=tasks[j-1].text
                web_task=tasks[j-1].find_element_by_tag_name('a')
                task_web[j-1]=web_task.get_attribute('href')
            print(len(task_dict)+1,':',"UPLOADS")
            task_dict[len(task_dict)]="UPLOADS"
            t=int(input('Type the task index from mentioned>'))
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
                      print(driver.find_element_by_xpath(full2).text,end=' ')
                except:
                  #driver2.get(task_web[t-1])
                  print("Your required task is done, there is nothing to show")
            else:
                d=int(input('Specify date to get uploads(01-31)>'))
                mon=input('Specify Month (eg. February)>')
                upload_date=driver.find_elements_by_class_name("sectionname")
                up_doc=driver.find_elements_by_class_name('content')
        
                ind=4
                z=2
                for k in range(1,len(up_doc)+1):

                  if ((mon in upload_date[ind-1].text)and((d<=int(upload_date[ind-1].text[:1]))or(d>=int(upload_date[ind-1].text.split('-')[1][1:2])))):
                    try:
                      doc=up_doc[z-1].find_elements_by_class_name("activityinstance")
                      print('These are the uploads for',d,mon)
                      for l in doc:
                        print(l.text)
                    except:
                      print("NO uploads for the provided date")
                    break
                  ind+=2
                  z+=1 
        except:
            print("your login time out")
            log=0
        #print(log)
        log=int(input("Anything else if yes write 1 else write 0>"))
                   
else:
    print("You must be logged in to your account. Please login first")  
