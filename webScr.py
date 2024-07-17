import requests
from bs4 import BeautifulSoup
import os
from os import path
import re

 
def get_base_url(url):
    index = url.rfind('/')
    return url[:index+1]

 
def write_to_local_file(text,dest,ext):
    if os.path.isfile(dest):
        os.remove(dest)
    f = open(dest,'w+')
    f.write(text)
    f.flush()
    f.close()

 
def get_file_name(url):
    index = url.rfind('/')
    return url[index+1:]        

 
base_url = 'https://people.sc.fsu.edu/~jburkardt/'
response = requests.get(base_url)
soup = BeautifulSoup(response.content,'html.parser')

 
src_lang_list = ['c software','c++ software','fortran90 software', 'python software']
lang_url_list = list()
#for all achor tags we get the link of our concerned languages
for link in soup.find_all('a'):
    if link.get_text().strip() in src_lang_list:
        print(base_url + link.get('href'))
        lang_url_list.append(base_url + link.get('href'))

src_files_url = list()
for lang_url in lang_url_list:
    #print(lang_url)
    response = requests.get(lang_url)
    base_lang_url = get_base_url(lang_url)
    soup_lang = BeautifulSoup(response.content,'html.parser')
    for link in soup_lang.find_all('a'):
        src_files_url.append(base_lang_url + link.get('href'))        

# maintain separate list for each source code files of language
src_files_c = []
src_files_cpp = []
src_files_py = []
src_files_forton90 = []
count = 0
for src_file_link in src_files_url:
    response = requests.get(src_file_link)
    base_file_url = get_base_url(src_file_link)
    print(base_file_url)
    soup_file_content = BeautifulSoup(response.content,'html.parser')
    count +=1
    for src_link in soup_file_content.find_all('a'):
        
        if type(src_link) != str() and src_link.has_attr('href'):
            if src_link['href'].lower().endswith('.c'):
                src_files_c.append(base_file_url + src_link.get('href'))
            elif src_link['href'].lower().endswith('.cpp'):
                src_files_cpp.append(base_file_url + src_link.get('href'))
            elif src_link['href'].lower().endswith('.py'):
                src_files_py.append(base_file_url + src_link.get('href'))
            elif src_link['href'].lower().endswith('.f90'):
                src_files_forton90.append(base_file_url + src_link.get('href')) 
    #print(count)   
            
src_files = src_files_c + src_files_cpp  + src_files_forton90  + src_files_py

 
cur_dir = os.getcwd()
cur_dir = cur_dir + r'\\'
for f in src_files:
    print(f)
    soup_for_actual_source_code = BeautifulSoup(requests.get(f).content,'html.parser')
    file_name = get_file_name(f)
    text = str(soup_for_actual_source_code)    
    if file_name.lower().endswith('.c'):
        dest = cur_dir + r"c source files" 
    elif  file_name.lower().endswith('.cpp'):
        dest = cur_dir + r"cpp source files" 
    elif  file_name.lower().endswith('.py'):
        dest = cur_dir + r"python source files" 
    elif  file_name.lower().endswith('.f90'):
        dest = cur_dir + r"forton90 source files" 
    # before directory creation, make sure that the directory does not exists.
    if os.path.exists(dest) == False:
        os.mkdir(dest)
    try:
        write_to_local_file(text,dest + '\\' + file_name,'c')
    except:
        print('exception occurs in file :{}'.format(file_name) )
print('all sources code files are downloaded successfully.')