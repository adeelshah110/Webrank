
from nltk.corpus import stopwords
STP_SET_ENG_NLTK = set(stopwords.words("english"))
import Web_Rank_v1 as WR1
import sys

    
def WebRank(URL):    
    Text,HTML = WR1.Web(URL)
    detected_language = WR1.detect_language(Text)
    name,stop_words =WR1.extract_stop_words(detected_language)
    
    URL_H_dic,URL_Q_dic = WR1.Divide_URL_HOST_QUERY (URL)
    h1_dic, h2_dic,h3_dic,h4_dic,h5_dic,h6_dic,A_dic,title_dic = WR1.Extract_headerAnchorTitle(HTML)
    
    
    candidate_list = WR1.Text_Clean(Text,stop_words)
    candidate_dic= WR1.COUNTER_DICT(candidate_list)
    unique_candidate_list =[]
    [unique_candidate_list.append(x) for x in candidate_list if x not in unique_candidate_list if x not in STP_SET_ENG_NLTK and x not in stop_words and len(x)>1 and x.isalpha()]
    
    
    string="Word,Relative Frequency %,H1%,H2%,H3%,H4%,H5%,H6%,Anchor%,Title%,Url-Host,Url-Query,GT,web-id";
    for word in unique_candidate_list:
        try:
            fr = candidate_dic.get(word)
            if fr is None or not fr:

                fr =0
                
            f1,f2,f3,f4,f5,f6,f7,f8,f9,f10 = WR1.GET_SCORE_EACH_FEATURE(word,h1_dic, h2_dic,h3_dic,h4_dic,h5_dic,h6_dic,A_dic,title_dic,URL_H_dic,URL_Q_dic)
            f12 = 0
            f11 =0
            string+="\n"+word+",";
            string+=str(fr)+",";
            string+=str(f1)+",";
            string+=str(f2)+",";
            string+=str(f3)+",";
            string+=str(f4)+",";
            string+=str(f5)+",";
            string+=str(f6)+",";
            string+=str(f7)+",";
            string+=str(f8)+",";
            string+=str(f9)+",";
            string+=str(f10)+",";
            string+=str(f11)+",";
            string+=str(f12);
        except:
            continue
    return (string,Text)
#########################################################



