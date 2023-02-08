#change
 
import sys
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib64/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/lib/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/titler/mt/lib/python3.4/site-packages/')
sys.path.append('/home/tko/himat/packages/')
from collections import defaultdict 
import re 
from nltk.corpus import stopwords
import numpy as np
import lxml
import math
import quandl
import urllib
import nltk
import quandl
import numpy as np
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import pandas as pd 
import math
import textwrap
import sys
import re 
from nltk.corpus import stopwords
import numpy as np
import nltk
import urllib
from bs4 import BeautifulSoup
import numpy as np
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import pandas as pd 
import math
import textwrap
import sys
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import defaultdict,Counter
sys.path.insert(0, '/home/tko/himat/web-docs/keywordextraction')

from flask import Flask
import requests
from bs4 import BeautifulSoup
import numpy as np

sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/')

sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/')

common_nouns ="january debt est dec big than who use jun jan feb mar apr may jul agust dec oct nov sep dec  product continue one two three four five please thanks find helpful week job experience women girl apology read show eve  knowledge benefit appointment street way staff salon discount gift cost thing world close party love letters rewards offers special close  page week dollars voucher gifts vouchers welcome therefore march nights need name pleasure show sisters thank menu today always time needs welcome march february april may june jully aguast september october november december day year month minute second secodns".split(" ")
# especial characters
spchars = re.compile('\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\+|\=|\\|\||\{|\[|\]|\}|\:|\;|\'|\"|\<|\,|\>|\?|\/|\.|\-')

#stopwords list
#english_stopwords=set(stopwords.words("english"))




##########################################################################################################
def Clean_text(text,Stopword_List):
    Words =[]
    for word in text.split():       
        word = word.replace("’",' ')
        word = word.lower()
        word = spchars.sub(" ",word.strip())
        if word not in Stopword_List:
            if word not in common_nouns:
                if len(word)>1:

                    if word != "  ":
                        if word not in common_nouns:
                            if not word.isdigit():
                                if word not in Stopword_List:
                                    for x in word.split():
                                        if x not in Stopword_List and x not in common_nouns and len(x)>1 and x not in common_nouns:
                                            x = x.strip()
                                            if not x[0].isdigit():                                        
                                                    



                                                Words.append(x)                                  

    return (Words)
###################################################################################################################              
                  
# Input read from the txt file 
file_open = open ('io/url.txt','r')
url = file_open.readline()
file_open.close()
#####################################################################################


###########################################################

   
import WebRank as WR

features,Text2 = WR.WebRank(str(url))

 
    

def Write(Text):
    words =' '
    for x in Text.split():        
        text = ''.join (x)        
        words += text+' '        
    return (words)
def Write_Text(Text):    
    text_words =Write(Text)           
    good_text =textwrap.fill(text_words,140)    
    k =open('io/Text.txt','w', encoding="utf-8-sig")
    
    k.write(str(good_text))    
    k.close()
###################################################################
Write_Text(Text2)
##############################################################
k = open ('io/Keywords.txt','w',encoding='utf-8-sig')
print (Text2,file =k)
k.close()
     
##################################################################

#############################################################################
#Write_Score_txt(wrd_fr_Tgs_Fnl_score)
###############################################################################
f = open ('io/Score.txt','w',encoding="utf-8-sig")
print (features,file=f)
f.close()
print ('fine')