import requests
import re
import sys
from tld import get_tld
import time

#你的爱站api
api = '88487e2a266a72255048e8202d506305'


def echoMessage():
    version = """  
      [#] Create By ::
        _                     _    ___   __   ____                             
       / \   _ __   __ _  ___| |  / _ \ / _| |  _ \  ___ _ __ ___   ___  _ __  
      / _ \ | '_ \ / _` |/ _ \ | | | | | |_  | | | |/ _ \ '_ ` _ \ / _ \| '_ \ 
     / ___ \| | | | (_| |  __/ | | |_| |  _| | |_| |  __/ | | | | | (_) | | | |
    /_/   \_\_| |_|\__, |\___|_|  \___/|_|   |____/ \___|_| |_| |_|\___/|_| |_|
                   |___/            By https://aodsec.com                                           
    """
    print(version)

def saveMessage(content, file):
    fp = open(file, 'a+', encoding='utf-8-sig')
    fp.write(content + "\n")
    fp.close()

def get_domain_rank(domain):
    rank_pc = "0"
    rank_m = "0"
    rank_google = "0"
    try:
        response = requests.get('https://apistore.aizhan.com/baidurank/siteinfos/' + AIZHAN_API + '?domains=' + domain)
        rank_pc = str(re.search('"pc_br":(.+),"m_br', response.text).group(1))
        rank_m = str(re.search('"m_br":(.+),"ip', response.text).group(1))
    except:
        pass
    try:
        res_google = requests.get("https://pr.aizhan.com/{}/".format(domain), timeout=10).text
        result_pc = re.findall(re.compile(r'<span>谷歌PR：</span><a>(.*?)/></a>'), res_google)[0]
        rank_google = result_pc.split('alt="')[1].split('"')[0].strip()
    except:
        pass
        
    print(domain+"rank_pc is "+rank_pc+";rank_m is "+rank_m+";rank_google is "+rank_google)
    if (int(rank_pc) > 0) or (int(rank_m) > 0 ) or (int(rank_google) > 2 ):
        saveMessage(domain, 'domain_rank.txt')
    else:
        pass
    time.sleep(1)

def removeDup(FileList):
    tmp_list=[]
    for i in FileList:
        j = getDomain(i)
        if j not in tmp_list:
            tmp_list.append(j)
        else:
            pass
    return tmp_list

def getDomain(url):
    res = ""
    try:
        res =get_tld(url, as_object=True).parsed_url.netloc
    except:
        res = "baidu.com"
    return res

if __name__ == '__main__':
    echoMessage()
    if len(sys.argv) != 2:
        print("usage:\n\tpython3 RankQuery.py domain.txt")
    else:
        domain_file = sys.argv[1]
        domain_txt = open(domain_file, 'r', encoding='utf-8').read().split('\n')
        domain_list = removeDup(domain_txt)
        print(domain_list)
        for domain in domain_list:
            print(domain)
            get_domain_rank(domain)
