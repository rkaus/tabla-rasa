import os
import re
import requests
from bs4 import BeautifulSoup
from more_itertools import unique_everseen
from string import punctuation
import pandas as pd

def chandra_bols():
    r = requests.get('http://www.chandrakantha.com/tablasite/comp/16/chakradar1.html')

    soup = BeautifulSoup(r.content)

    pre = soup.find_all('pre')
    summary = soup.findAll('tr',{'class':'nohighlight'})
    comments = soup.findAll('td',{'colspan':'6'})
    return pre, summary, comments


def chandra_link_grabber():

    r = requests.get('http://www.chandrakantha.com/tablasite/comp/12/')
    soup = BeautifulSoup(r.content,'lxml')

    links = soup.findAll('a')



def musicking():
    #40
    r = requests.get('http://www.musicking.gr/tabla_compositions/?lang=en')
    soup = BeautifulSoup(r.content, 'lxml')

    links = soup.findAll('li')
    stubs = []
    for l in links:
        al = l.find('a')
        # import pdb; pdb.set_trace()
        stubs.append(al['href'])

    urls = []
    bad_urls = []
    # import pdb; pdb.set_trace()
    for stub in stubs:
        if '\u' not in stub:
            # import pdb; pdb.set_trace()
            u = 'http://www.musicking.gr%s' % stub
            urls.append(u)
        else:
            bad_urls.append(stub)


    for url in urls:
        #scrape each page
        if type(url) == unicode:
            bad_urls.append(url)
        else:
            page = requests.get(url)
            soup = BeautifulSoup(page.content,'lxml')
            # import pdb; pdb.set_trace()
            ess = soup.findAll('td',{'width':'3%'})
            for stroke in ess:
                "".join(stroke.text)


    return links, bad_urls, urls

def tablapedia():
    #130 bols
    #TODO: get difficulty for each bol

    r = requests.get('http://www.tablapedia.org/')
    soup = BeautifulSoup(r.content,'lxml')
    a = soup.findAll('a',{'href':True})

    urls = []
    for each in a:
        if each.parent.name == 'td':
            url = 'http://www.tablapedia.org{}'.format(each['href'])
            urls.append(url)

    al = soup.findAll('a')
    details = []
    for each in al:
        if each.parent.name == 'td':
            details.append(each.text)


    # ttl = []
    composition = []
    about = []
    for url in unique_everseen(urls):
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        # import pdb; pdb.set_trace()

        # taal = typ = lvl = []
        # bs = soup.findAll('b')
        #
        # if len(bs) == 3:
        #     z = soup.find('b')
        #     if z == 'Taal:':
        #         taal.append(z.next_sibling.strip())
        #     else:
        #         taal.append(0)
        #
        #
        #     x = z.find_next('b')
        #     if x and x.text == 'Type:':
        #         typ.append(x.next_sibling.strip())
        #     else:
        #         typ.append(0)
        #
        #     # try:
        #     c = x.find_next('b')
        #     if c and c.text == 'Difficulty:':
        #         lvl.append(c.next_sibling.strip())
        #     else:
        #         lvl.append(0)
        #
        # if len(bs) == 2:
        #     z = soup.find('b')
        #     if z == 'Taal:':
        #         taal.append(z.next_sibling.strip())
        #     else:
        #         taal.append(0)
        #
        #
        #     x = z.find_next('b')
        #     if x and x.text == 'Type:':
        #         typ.append(x.next_sibling.strip())
        #     else:
        #         typ.append(0)
        #
        # if len(bs) == 1:
        #     z = soup.find('b')
        #     if z == 'Taal:':
        #         taal.append(z.next_sibling.strip())
        #     else:
        #         taal.append(0)

        #extract compositon from js vars
        # import pdb; pdb.set_trace()
        st = soup.findAll('script')[1].string
        p = re.compile('var composition = (.*);')
        m = p.search(st)
        if m:
            m1 = m.group(1)
            cc = re.findall(r'"(.*?)"', m1)
            composition.append(cc)

        about.append(soup.find('div',{'class':'about'}).text)

    # for i in range(129):
    #     url = 'http://www.tablapedia.org/compositions/{}'.format(i+1)
    #     r = requests.get(url)
    #     soup = BeautifulSoup(r.content,'lxml')
    #
    #     for b in soup.findAll('b'):
    #         ttl.append(b.next_sibling.strip())
    #
    #     #extract compositon from js vars
    #     st = soup.findAll('script')[1].string
    #     p = re.compile('var composition = (.*);')
    #     m = p.search(st)
    #     if m:
    #         composition.append(m.group(1))

    return soup, composition, details, about

def austin_bols():
    #220
    with open('austin_comp_db.html','r') as a:
        soup = BeautifulSoup(a, 'lxml')
    return soup


def read_bols():
    df = pd.DataFrame()
    tdf = None
    path = '/home/rkaus/galvanize/Project/tabla/upf_data/score'
    for f in os.listdir(path):
        p = path + '/{}'.format(f)
        tdf = pd.read_table(p)
        df = df.append(tdf.T)

    col_names = {0:'gharana',1:'number',2:'jati',3:'type',4:'taal',5:'composer'}
    df = df.rename(index=str, columns=col_names)

    df.gharana = [x[8:] for x in df.gharana]
    df.number = [x[12:] for x in df.number]
    df.jati = [x[5:] for x in df.jati]
    df.type = [x[5:] for x in df.type]
    df.taal = [x[5:] for x in df.taal]
    df.composer = [x[9:] for x in df.composer]
    # df[0] = [x[8:] for x in df[0]]
    # import pdb; pdb.set_trace()
    df['comp_string'] = df.ix[:,9:].astype(str).sum(axis=1)
    # df['']
    # for i in range(len(df)):
    #     df.ix[i].comp_string = df.ix[i].comp_string.replace(',',' ')

    df.comp_string = df.comp_string.str.replace(';', ' ')
    df.comp_string = df.comp_string.str.replace(',', ' ')
    df.comp_string = df.comp_string.str.replace('nan','')
    df.comp_string = df.comp_string.str.replace('!E','')
    df.comp_string = 's1 s2 ' + df.comp_string + ' e1 e2 '

    tokens = df.comp_string.str.cat().split()
    tokens = [x for x in tokens if '!' not in x]
    tokens = [x for x in tokens if '\'' not in x]
    tokens = [x for x in tokens if 'D' not in x]
    tokens = [x for x in tokens if 'd' not in x]

    return tokens

def beat_dict():
    bd = pd.read_excel('beat_dict.xlsx')
    return bd


if __name__ == '__main__':
    # soup, composition, details, about = tablapedia()
    # links, bs, urls = musicking()
    # pre, summary, comments = chandra_bols()
    # ab = austin_bols()
    df = upf_bols()
    bd = beat_dict()
