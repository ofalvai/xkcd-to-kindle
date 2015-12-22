import os
from shutil import copy
import urllib.request
from bs4 import BeautifulSoup
import html
import subprocess
import sys

print('XKCD mobi generator')
first = int(input('First comic to download:\n'))
last = int(input('Last comic to download:\n'))
print('Downloading comics...')

if not os.path.exists('out/img'):
    os.makedirs('out/img')
if os.path.exists('out/xkcd.html'):
    os.remove('out/xkcd.html')
if os.path.exists('out/toc.html'):
    os.remove('out/toc.html')
if os.path.exists('out/metadata.opf'):
    os.remove('out/metadata.opf')
if os.path.exists('out/kindlegen_log.txt'):
    os.remove('out/kindlegen_log.txt')

copy('assets/toc_empty.ncx', 'out/toc.ncx')
copy('assets/metadata.opf', 'out/metadata.opf')

file_xkcd = open('out/xkcd.html', 'a', encoding='utf-8')
file_xkcd.write('<html><head><title>XKCD: {0} - {1}</title></head><body>'.format(first, last))

file_toc = open('out/toc.html', 'a', encoding='utf-8')
file_toc.write('<html><body><a name="toc"></a><h3>TABLE OF CONTENTS</h3>')
toc_chunk = ''

file_ncx = open('out/toc.ncx', 'a', encoding='utf-8')
ncx_chunk = ''

# List of IDs of comics that would break the script... #404 is an obvious one :)
blacklist = [404, 1350, 1416, 1525, 1608]
failed = 0

for i in range(first, last + 1):
    if i in blacklist:
        continue
    if failed > 10:
        # Preventing an infinite loop (ie. the user gave a number bigger than the last comic)
        print('Download failed 10 times, moving on...')
        break
    try:
        page = urllib.request.urlopen('http://xkcd.com/' + str(i))
        soup = BeautifulSoup(page.read().decode('utf-8'), 'html.parser')
        el_comic = soup.find('div', id='comic')
        has_link = False
        if el_comic.find('a') and not i == 1005:
            # The comic is wrapped in a link:
            el_img = el_comic.a.img
            link = el_comic.a['href']
            has_link = True
        else:
            el_img = el_comic.img
        if i == 472:
            title = '472: House of pancakes'
        else:
            title = str(i) + ': ' + soup.find('div', id='ctitle').string
        print(title)

        # urllib can't handle the "//example.com" URL format: 
        img_file = urllib.request.urlopen('http:' + el_img['src']).read()
        file_img = open('out/img/' + str(i) + '.png', 'wb')
        file_img.write(img_file)
        file_img.close()
        text = html.escape(el_img['title'], True)
        if has_link:
            file_xkcd.write(('<a id="{0}"></a><h3>{1}</h3><p><img src="img/{0}.png" /></p>'
                + '<p>{2}</p><p>Link: <a href="{3}">{3}</a></p><mbp:pagebreak />')
                .format(i, title, text, link))
        else:
            file_xkcd.write('<a id="{0}"></a><h3>{1}</h3><p><img src="img/{0}.png" /></p><p>{2}</p><mbp:pagebreak />'
                .format(i, title, text))
        toc_chunk += '<p><a href="xkcd.html#{0}">{1}</a></p>'.format(i, title)
        ncx_chunk += ('<navPoint id="navpoint-{0}" playOrder="{0}"><navLabel><text>{1}</text>'
            + '</navLabel><content src="xkcd.html#{0}"/></navPoint>').format(i, title)
    except:
        print('Failed to download #{0}, skipping...'.format(i))
        failed += 1
        continue

file_xkcd.write('<mbp:pagebreak /></body></html>')
file_xkcd.close()
toc_chunk += '</body></html>'
file_toc.write(toc_chunk)
file_toc.close()
ncx_chunk += '</navMap></ncx>'
file_ncx.write(ncx_chunk)
file_ncx.close()

print('\nCreating .mobi file...')
with open('out/kindlegen_log.txt', 'w') as file_log:
    subprocess.call(['bin/kindlegen.exe', 'out/metadata.opf', '-o', 'xkcd.mobi'], stdout=file_log)
print('Ready...results are placed in "out" folder (images, xkcd.mobi, xkcd.html, kindlegen_log.txt)')

if os.path.exists('out/toc.html'):
    os.remove('out/toc.html')
if os.path.exists('out/metadata.opf'):
    os.remove('out/metadata.opf')
if os.path.exists('out/toc.ncx'):
    os.remove('out/toc.ncx')

i = input('\nPress any key to exit\n')
sys.exit()
