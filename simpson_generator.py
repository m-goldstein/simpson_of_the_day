import requests
import random
import sys
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup as Soup
requests.urllib3.disable_warnings()

# params:
#   x -> string : name
#   y -> list : list of Simpsons objects
find_simpsons_by_name = lambda x,y: [e for e in y if x in e.name]

# params:
#   x -> string : name
#   y -> list of tuples : (charachter,url) pairs in list
find_imgs_by_name = lambda x,y: [e[1] for e in y if x in e[0]]

to_datetime = lambda x: datetime.strptime(x, DATE_FMTSTRING)
to_datetimestr = lambda x: x.strftime(DATE_FMTSTRING)

LIST_URL = "https://simpsons.fandom.com/wiki/Portal:All_Simpson_Characters"
_WIKIA_GALLERY_ITEM = 'wikia-gallery-item'
_REVISION = '/revision'
DATE_FMTSTRING = '%m/%d/%Y'
ASSET_DIR = './assets/'
SEEN_FP = f'{ASSET_DIR}seen'
REGEX = r'(\w+)(\.\w+)+(?!.*(\w+)(\.\w+)+)'
IMG_DIR = './biopics/'
DELIM = ':'

chrs = None
seen = None


def debug(m, **args):
    #print(m, **args)
    pass

class Simpson:
    def __init__(self,name=None,date=None,seen=False,path=None):
        self.name = name
        self.date = date
        self.path = path
        self.seen = seen
    
    def __str__(self):
        return f'Name: {self.name} - Date: {self.date} - Image Path: {self.path} - Seen: {self.seen}'

def do_request(url=None, method='GET', verify=False, **args):
    if method == 'GET':
        func = requests.get
    elif method == 'POST':
        func = requests.post
    else:
        print (f'not implemented {method=}')
        return None
    try:
        return func(url=url,verify=verify, **args)
    except Exception as e:
        print(f'Exception: {e}')
        return None


def load_seen_map(seen_fp=SEEN_FP,DELIM=':'):
    seen = []
    global chrs
    try:
        fp = open(seen_fp,'r')
        body = fp.read()
        fp.close()
    except Exception as e:
        print(f'Exception: {e}; could not open {seen_fp}')

    elems = [e.lstrip().rstrip() for e in body.split('\n') if len(e.lstrip().rstrip())]
    
    for e in elems:
        name,date = e.split(DELIM)
        date = to_datetime(date)
        imgpath = find_imgs_by_name(name,chrs)
        if len(imgpath) == 0:
            imgpath = ''
        elif len(imgpath) == 1:
            imgpath = imgpath[0]
        else:
            imgpath = imgpath[0]
        s = Simpson(name=name,date=to_datetimestr(date),path=imgpath,seen=True)
        seen += [s]
    
    return seen

def get_charachters_and_images(use_net=True,infile=f'{ASSET_DIR}charachters_and_images', outfile=None,DELIM=':'):
    charachters = []
    _charachters = []
    if use_net:
        body = do_request(url=LIST_URL)
        soup = Soup(body.text,'html.parser')
        gala = [e for e in soup.find_all('div') if e.has_attr('class') and _WIKIA_GALLERY_ITEM in e.attrs['class']]
        _charachters = [(e.get_text(),e.img.attrs['src']) for e in gala]
    elif not use_net:
        try:
            fp = open(infile,'r')
            body = fp.read()
            fp.close()
        except Exception as e:
            print(f'Exception: {e}; could not open {infile}')
            return None
        lines = [e.lstrip().rstrip() for e in body.split('\n') if len(e.lstrip().rstrip())]
        for l in lines:
            idx = l.find(DELIM)
            e = l[:idx]
            f = l[idx+1:]
            _charachters += [(e,f)]
        return _charachters

    for i in range(len(_charachters)):
        ch = _charachters[i]
        _,url = ch
        idx = url.find(_REVISION)
        imgname = [e for e in re.finditer(REGEX,url)][0].group()
        fname = f'{IMG_DIR}{imgname}'
        if idx < 0:
            pass
        else:
            url = url[:idx]
        if use_net:
            r = do_request(url=url)
            if r.status_code == 200:
                imgdata = r.content
                try:
                    fp = open(fname,'wb')
                    fp.write(imgdata)
                    fp.close()
                    charachters += [(_,fname)]
                except Exception as e:
                    print(f'Exception: {e}; could not open {fname} for I/O')
                    charachters += [(_,url)]
            else:
                charachters += [(_,url)]
            print(f'fetching details: {i}/{len(_charachters)}...',end='\r')
        else:
            charachters += [(_,url)]
    print('')
    if outfile:
        fp = open(f'{outfile}','w')
        for ch in charachters:
            e,f = ch
            fp.write(f'{e}{DELIM}{f}\n')
        fp.close()
    return charachters


def update_seen_list(charachter=None,seen_fp=SEEN_FP,DELIM=':'):
    fp = open(seen_fp,'w')
    global seen
    
    for ch in seen:
        name,date = ch.name,ch.date
        fp.write(f'{name}{DELIM}{date}\n')
    
    if charachter:
        name = charachter.name
        date = charachter.date
        fmt = f'{name}{DELIM}{date}\n'
        fp.write(fmt)
    
    fp.close()
    seen = load_seen_map(DELIM=DELIM)

def get_random_charachter(use_net=False):
    flag = False
    global seen
    global chrs
    if seen is None:
        seen = load_seen_map() 
    if chrs is None:
        chrs = get_charachters_and_images(use_net=use_net)
    seen_chrs = [(e.name,e.path) for e in seen]
    
    while not flag:
        choice = random.choice(chrs)
        if choice in seen_chrs:
            continue
        else:
            flag = True
            name = choice[0]
            path = choice[1]
            s = Simpson(name=name, date=datetime.now().strftime(DATE_FMTSTRING),path=path,seen=True)
            seen += [s]
            update_seen_list()
            return s.name,s.path

def init_and_get_random_charachter(use_net=False):
    global chrs
    global seen
    if chrs is None:
        chrs = get_charachters_and_images(use_net=use_net)
    if seen is None:
        seen = load_seen_map()
    return get_random_charachter(use_net=use_net)
