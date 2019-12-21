#JobSploit by Mori
#this script will send "your" resume to thousands of job listings
#to a specific job title and city, regardless of qualifications.
#who even is qualified nowadays anyways.

#CAUTION:
#you will probably recieve a lot of spam from in you inbox as a result
#or get blacklisted from something running it multiple times with the same query
#would recommend using a throwaway email account and running on a cloud server


from bs4 import BeautifulSoup
import requests
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io


#function to extract text from a PDF
def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    return data

#send the request with necesssary data
def applyto(url, first, last, email, filepath):
    #assuming most resumes will be in PDF format
    text = pdfparser(filepath)
    
    data = {'firstname':first, 
            'lastname':last, 
            'email':email, 
            'copy_paste':text} 
    response = requests.post(url, data=data)
    print("-- resume sent -- ")

job = input('what job title are you looking for (ex:software developer)? ')
location = input('what city are you looking for a job in? ')
first = input('enter your first name: ')
first.title()
last = input('enter your lastname: ')
last.title()
email = input('enter your email address: ')
resumepath = input('enter the full path to your resume: ')


print("hammering away....this may take a bit..")

#format query strings for location and job title
job.replace(' ', '+')
print("job query is: ", job)
location.replace(' ', '+')
print("location query is: ", location)

#url adapted from indeed.com
new_url = 'https://www.careerbuilder.com/jobs?keywords=' + job + '&location=' + location
page_response = requests.get(new_url, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")

jobs = []
index = 0
for link in page_content.find_all("span"):
   jobs.append(link.text)
#    print(link.text)

#get the links to apply
apply_urls = []
for link in page_content.find_all("a"):
    job_id = link.get("data-job-did")
    if str(job_id) != "None":
        print("applying to: ", jobs[index])
        index += 1
        print("located in: ", jobs[index])
        index += 1
        print("position: ", jobs[index])
        index += 1
        #print("job id:", job_id)
        print("")
        apply_url = "https://www.careerbuilder.com/apply/" + job_id + "/submit"
        applyto(apply_url, first, last, email, resumepath)
        apply_urls.append(apply_url)
    

print(apply_urls)