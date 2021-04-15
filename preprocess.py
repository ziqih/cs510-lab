import html2text
from os import listdir
from os.path import isfile, join

path = 'clef-code/crawl/warc/'
dirs = [f for f in listdir(path)]

h = html2text.HTML2Text()
h.ignore_links = True
h.IGNORE_IMAGES = True
h.PROTECT_LINKS = True
h.IGNORE_TABLES = True
h.ESCAPE_SNOB = True

n, error = 0, 0
for i in dirs:
    if i[0] == '.':
        continue
    path2 = path + i + '/'
    files = [f for f in listdir(path2)]
    print(path2)
    for j in files:
        n += 1
        if n % 20 == 0:
            print(n, error)
        try:
            file_path = path2 + j
            a = ''
            file_str = open(file_path, 'r', encoding='utf8')
            for k in file_str.readlines():
                a += k

            r = h.handle(a)
            r = r.split('\n')
            res = []
            for k in r:
                while '  ' in k:
                    k = k.replace('  ', '')
                if k.count(' ') > 6:
                    res.append(k)
            # print(res)

            f = open('bm25/input/' + i + '_' + j, 'w')
            for k in res:
                f.write(k + '\n')
        except:
            error += 1

