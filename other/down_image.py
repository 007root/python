'''
download image from oss
down.txt content
...
aew3212.png
reoi342.png
...
'''
import os
import multiprocessing
import requests


save_dir = '/data/images/'
down_url = 'http://aliyuncs.com/gofunapi/images/'


def write_file(file_url, ret):
    with open(file_url, 'wb') as f:
        f.write(ret.content)


def download(name):
    url = down_url + name
    try:
        ret = requests.get(url)
        if ret.status_code != 200:
            with open('err', 'a') as f:
                f.write(url + ' ' + str(ret.status_code) + '\n')
            return
        file_url = save_dir + name
        write_file(file_url, ret)
    except IOError:
        os.mkdir(save_dir + file_url.split('/')[-2])
        write_file(file_url, ret)
    except Exception as e:
        with open('err', 'a') as f:
            f.write(url + ' %s' % e +'\n')


if __name__ == '__main__':
   with open('down.txt') as f:
       data = f.read()
       im = data.strip('\n').split('\n')
   num = len(im)
   sep = 0
   count = 0
   while sep < num:
       sep += 100
       for name in im[count:sep]:
           url = down_url + name
           p = multiprocessing.Process(target=download, args=(name,))
           p.start()
       print(sep)
       count = sep
