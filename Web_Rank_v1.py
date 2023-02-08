import sys
'''
sys.path.append('/home/tko/himat/web-docs/lib/python3.6/site-packages/')
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib64/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/lib/python3.6/site-packages/lib64/python3.6/site-packages')
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/lib/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/lib/python3.6/site-packages/')
sys.path.append('/home/tko/himat/lib/python3.4/site-packages/')
#NEW LOCATION FOR PACKAGES ON SERVER
sys.path.append('/home/tko/himat/web-docs/keywordextraction/lib/python3.6/site-packages')
sys.path.append('/usr/lib/python3.4/site-packages')
sys.path.insert(0, '/home/tko/himat/web-docs/keywordextraction')
sys.path.append('/home/tko/himat/packages/')'''

from collections import defaultdict 
import re 
from nltk.corpus import stopwords
STP_SET_ENG_NLTK = set(stopwords.words("english"))
import numpy as np
import lxml
import sys
import math
import urllib
import nltk
import numpy as np
from nltk import word_tokenize
import sys
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import defaultdict,Counter
F_stopwords = set(stopwords.words("finnish"))
url_unused_words = ['','https','www','com','-','php','pk','fi','https:','http','http:','html','htm']
english_stop_words =[x for x in STP_SET_ENG_NLTK]
finnish_stop_words =[x for x in F_stopwords]
combine_stopwords = english_stop_words + finnish_stop_words
#####################################################################################
def Read_file(name):
    html = ''
    with open (name,'r',encoding ='utf-8-sig',errors='ignore') as f:
        read_txt = f.readlines()
        if name == 'text_file':
            txt =[x for x in read_txt.split('\n')]
            
            return (txt)
        else:
            for x in read_txt:
                x=x.strip('\n')
                html +=x
            return (html)
def Read_Txt(file):
    f=open(file,'r',encoding ='utf-8-sig',errors='ignore')
    read = f.readlines()
    f.close()
    gt =[]
    for x in read:
        URL= (x.split()[0])
        Gt =x.replace(URL,'')
               
        for y in Gt.split():
            y =y.strip("\n")
            y=y.strip(",")
            if y==" " or y is None:
                continue
            gt.append(y.lower())            
    return(URL,gt)  

################################################################################################
def Reading_text_HTML(text_file):    
    text_file =open (text_file,'r',encoding ='utf-8-sig',errors='ignore')    
    read_text =text_file.readlines()   
    text_file.close()    
    lines = (line.strip() for line in read_text)    # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))# break multi-headlines into a line each
    return u'\n'.join(chunk for chunk in chunks if chunk)
#####################################################################################################
def Read_Combine_txt(root,ds_name,index,N):	
    base = root + ds_name[N] + '/' + str(index) + '/'
    txt_file = base + 'Text.txt'
    HTML_file = base + 'HTML.txt' 
    GT_file = base + 'GT.txt'
    URL_file = base + 'URL.txt'
   
    Text = Reading_text_HTML(txt_file)
    URL =Reading_text_HTML(URL_file)
    GT =Reading_text_HTML(GT_file)    
    
    
    HTML =  Read_file(HTML_file)
    HTML = BeautifulSoup(HTML, 'lxml')
    return (URL,GT,Text,HTML)

def Read_Combine_txt2(root,index,N):	
    base = root + str(index) + '/'
    txt_file = base + 'Text.txt'
    HTML_file = base + 'HTML.txt' 
    GT_file = base + 'Tags.txt'  
    Text = Reading_text_HTML(txt_file)
    
    URL,GT =Read_Txt(GT_file)    
    
    
    HTML =  Read_file(HTML_file)
    HTML = BeautifulSoup(HTML, 'lxml')
    return (URL ,GT,Text,HTML)

def Read_Combine_txt3(root,index,N):	
    base = root + str(index) + '/'
    txt_file = base + 'Text.txt'
    HTML_file = base + 'HTML.txt' 
    GT_file = base + 'GT.txt'
    URL_file = base + 'URL.txt'
   
    Text = Reading_text_HTML(txt_file)
    URL =Reading_text_HTML(URL_file)
    GT =Reading_text_HTML(GT_file)    
    
    
    HTML =  Read_file(HTML_file)
    HTML = BeautifulSoup(HTML, 'lxml')
    return (URL,GT,Text,HTML)
####################################################################################################
def GT_selection(GT,N):
    gt = []
    
    if N ==2:
        for x in GT.split(","):
            for i in x.split(" "):
                i = i.replace('[','').replace(']','').replace(')','').replace('(','').replace("'",'').replace(',','').strip()
                if len(i)>2 and i not in STP_SET_ENG_NLTK:
                    if i.isalpha():
                        gt.append(i)
    else:
        [gt.append(x) for x in GT.split(',') if x not in STP_SET_ENG_NLTK and len(x)>1 and x.isalpha()]
    return (gt)
###########################################################################################


def COUNTER_DICT(list_words):
    score_dic ={}
    if len (list_words)>=1:
        list_words = [x for x in list_words if x not in combine_stopwords and len(str(x))>1 and str(x).isalpha() ]
        word_count_dict ={}
        unique_list =[]
        [unique_list.append(x) for x in list_words if x not in unique_list]
        lngth_list = len(unique_list)
        counter_list = Counter(list_words)
        word_fr_dic ={}
        
        for word,fr in counter_list.most_common():
            word_fr_dic[word]= fr
        for word in unique_list:
            fr = word_fr_dic.get(word)    
            fr_word = fr/lngth_list
            
            score_dic[word]= fr_word
        return (score_dic)
    else:
        
        return ()


def Divide_Url(url):
    
    from urllib.parse import urlparse 
    host=[]
    obj=urlparse(url)    
    name =(obj.hostname)
    for x in name.split('.'):
        if x.lower() not in url_unused_words:
            host.append(x)
    return(host)
def Divide_URL_HOST_QUERY (URL):
    path=[]
    host =Divide_Url(URL)   
    for x in URL.split('/'):
        for i in x.split('.'):
            for d in i.split('-'):
                if d.lower() not in url_unused_words and d.lower() not in host:              

                   path.append(d.lower())
    host_dic = COUNTER_DICT(host)
    path_dic = COUNTER_DICT(path)
    return(host_dic,path_dic)
################################################################################################

        

def get_text(soup,h):
    text=[]
    text2 =[]
    text_dic ={}
    
    for w in soup.find_all(h):
        h_text = w.text.strip()
        h_text =h_text.replace(':','') #change made here
        h_text =h_text.replace(',','')
        h_text =h_text.replace('|','')
        h_text =(h_text.lower())
        #change made here 
       
        for x in h_text.split('-'):
            text.append(x)
            
    if len(text)!=0:
        for x in text:
            word=[n.strip() for n in x.split(',')]
            for x in word:
                words=[i.strip() for i in x.split() ]
                for x in words:
                    text2.append(x)
                    
        text_dic = COUNTER_DICT(text2)       
        return(text_dic)
    else:
        return(text_dic)

def CHEK_NULL(word,dic):
    f =0
    if len(dic)>=1:
        
        f = dic.get(word)
    else:
        f =0
    if f is None:
        f =0
    return (f)

def Extract_headerAnchorTitle(soup):   
    h1_d= get_text(soup,'h1')
    h2_d= get_text(soup,'h2')
    h3_d=get_text(soup,'h3')
    h4_d= get_text(soup,'h4')
    h5_d= get_text(soup,'h5')
    h6_d= get_text(soup,'h6')    
    a_d= get_text(soup,'a') #alt tab or anchor
    title_d= get_text(soup,'title')  #CALLing        
    return(h1_d,h2_d,h3_d,h4_d,h5_d,h6_d,a_d,title_d)
######################################################################################
def GET_SCORE_EACH_FEATURE(word,h1_dic, h2_dic,h3_dic,h4_dic,h5_dic,h6_dic,A_dic,title_dic,URL_H_dic,URL_Q_dic):
    f1 = CHEK_NULL(word,h1_dic)
    f2 = CHEK_NULL(word,h2_dic)
    f3 = CHEK_NULL(word,h3_dic)
    f4 = CHEK_NULL(word,h4_dic)
    f5 = CHEK_NULL(word,h5_dic)
    f6 = CHEK_NULL(word,h6_dic)
    f7 = CHEK_NULL(word,A_dic)
    f8 = CHEK_NULL(word,title_dic)
    f9 = CHEK_NULL(word,URL_H_dic)
    f10 = CHEK_NULL(word,URL_Q_dic)
    
    
    
    return (f1,f2,f3,f4,f5,f6,f7,f8,f9,f10)

def Clean_GT(GT):
    gt =[]
    for x in GT.split(","):
        for i in x.split(" "):
            i = i.replace('[','').replace(']','').replace(')','').replace('(','').replace("'",'').replace(',','').strip()
            if len(i)>2 and i not in combine_stopwords:
                if i.isalpha():
                    gt.append(i)  
    return (gt)
###################################################################################
def Scrapper1(element):
    if element.parent.name  in ['html','style', 'script']:
        return False
    if isinstance(element, Comment):
        return False
    return True
def Scrapper2(body):                #text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')      
    texts = soup.findAll(text=True)   
    name =soup.findAll(name=True) 
    visible_texts = filter(Scrapper1,texts)        
    return u" ".join(t.strip() for t in visible_texts)
#raw =Scrapper2(html)#text
def Scrapper3(text):                  #filters(text):  
    lines = (line.strip() for line in text.splitlines())    # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))# break multi-headlines into a line each
    return u'\n'.join(chunk for chunk in chunks if chunk)# drop blank lines
def Scrapper_title_4(urls):
  req = urllib.request.Request(urls, headers={'User-Agent' : "Magic Browser"}) 
  con = urllib.request.urlopen(req)
  html= con.read()  
  title=[]  
  soup = BeautifulSoup(html, 'lxml') 
  title.append(soup.title.string)
  return(title,urls)

def Web(urls):
  req = urllib.request.Request(urls, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()  
  soup = BeautifulSoup(html, 'lxml')  #keywordregex = re.compile('<meta\sname= ["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')  
  
  raw =Scrapper2(html)
  clean_text=Scrapper3(raw) 
  
  return(clean_text,soup)  

import sys

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print ('[!] You need to install nltk (http://nltk.org/index.html)')


#----------------------------------------------------------------------
def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}
    
    @param text: Text whose language want to be detected
    @type text: str
    
    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """

    languages_ratios = {}

    '''
    nltk.wordpunct_tokenize() splits all punctuations into separate tokens
    
    >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
    ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
    '''

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
       
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios


#----------------------------------------------------------------------
def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.
    
    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.
    
    @param text: Text whose language want to be detected
    @type text: str
    
    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)
    stop_words_for_language = set(stopwords.words(most_rated_language))
    

    return most_rated_language,stop_words_for_language



if __name__=='__main__':

   text = '''
   abc '''
    


#language = detect_language(text)
#print (language)

def extract_stop_words(detected_language):
    stop_words =[]
    language_name = detected_language[0]
    for x in detected_language:
        for i in x: 
            stop_words.append (i)
    return (language_name,stop_words)

def Text_Clean(Text,stopwords):
    clean_text =[]
    k=[]
    filter_text = [x.lower().strip().replace('.','').replace('‘','').replace('"','').replace('\'','').replace('?','').replace(',','').replace('-','').replace(':','').replace('!','').replace('@','').replace(')','').replace('(','').replace('#','').replace('%','').replace('"','').replace('/','').replace('\\','').replace('~','').replace('’','').replace('”','').replace(';','').replace('–','').replace('\\','').replace("  ",'').replace('/n','').replace('\n','').replace('…','').replace('“','').strip() for x in Text.split()]
    for word in filter_text:
        [clean_text.append(x)for x in word.split() if x not in stopwords and len(x)>1 and x.isalpha()]
        #[k.append(x) for x in word.split() if x not in stopwords and len(x)>1 and not x.isalpha()]
    #print (k)
    return(clean_text)