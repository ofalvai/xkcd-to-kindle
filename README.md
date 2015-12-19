#XKCD to Kindle#

![](https://dl.dropbox.com/u/2640488/cover.jpg)

A Python script that  downloads XKCD comics and converts them to a .mobi e-book using [Kindlegen.exe](http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211). Requires the BeautifulSoup module (`pip install beautifulsoup4`).

You can specify the first and the last comic to download. First it makes a HTML file of the comics, extracting the comic title, the comic itself, the alt text, and a link, if the comic contains one. A table of contents is also generated.

You can convert the .mobi to .epub if you want to, and you find every downloaded image in */src/img*.

Also, [here](https://dl.dropbox.com/u/2640488/XKCD-1-1152.mobi) is a generated e-book from ep. 1-1152.
