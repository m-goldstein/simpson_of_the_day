import sys
import os
from simpson_generator import init_and_get_random_charachter
from datetime import datetime
import requests
from bs4 import BeautifulSoup as soup

requests.urllib3.disable_warnings()
_ASSETS_DIR = './assets/'
_WWW_DIR = './www/'
_HTML_FNAME = f'index.html'
_HTML_FP = f'{_WWW_DIR}{_HTML_FNAME}'
DATE_FMTSTRING = '%m/%d/%Y'
ARCHIVE_DIR = './archive/{}/{}/'
_SEEN_FNAME = 'seen'
_SEEN_FP = f'{_ASSETS_DIR}{_SEEN_FNAME}'
_SEEN_BAK_FNAME = 'seen.bak'
_SEEN_BAK_FP = f'{_ASSETS_DIR}{_SEEN_BAK_FNAME}'
_SYNC_CMD = f'cp {_SEEN_BAK_FP} {_SEEN_FP}'
_html =\
"""<html>
<head>
<title>Simpson's character of the day!</title>
</head>
<body>
    <h1>Today's ({}) Character is {}!</h1>
    <img src={}>
</body>
</html>"""

def make_html(html=_html,html_fp=_HTML_FNAME,use_net=False,archive=True):
    date = datetime.now().strftime(DATE_FMTSTRING)
    name, imgpath = init_and_get_random_charachter(use_net=use_net)
    html = html.format(date,name,imgpath)
    fp = open(f'{_WWW_DIR}{html_fp}','w')
    fp.write(html)
    fp.close()
    if archive:
        date = datetime.now()
        archive_fp = f'{ARCHIVE_DIR.format(date.month,date.day)}{html_fp}'
        fp = open(archive_fp,'w')
        fp.write(html)
        fp.close()
    return html

if __name__ == '__main__':
    use_net = False
    if len(sys.argv) > 1:
        if '--sync' in [e.lower() for e in sys.argv[1:]]:
            os.system(_SYNC_CMD)
        if '--use-local' in [e.lower() for e in sys.argv[1:]]:
            use_net = False
        elif '--use-net' in [e.lower() for e in sys.argv[1:]]:
            use_net = True
        if '--today' in [e.lower() for e in sys.argv[1:]]:
            html = make_html(html=_html,use_net=use_net)
        if '--show' in [e.lower() for e in sys.argv[1:]]:
            os.system(f'open {_HTML_FP}')
