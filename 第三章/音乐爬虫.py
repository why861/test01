import requests
url='https://m704.music.126.net/20260626151713/c40a669af2813569216dbc4fc08a44bb/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/30589460575/b0cd/4bc3/127f/665adc0909830385d677a37fe6845eeb.m4a?vuutv=GrT4EZ8kkejOeXB0keb+c2u6epiRmUtTKzY5J/GdgxvgXiDUKvROn/fkmrDmyUOx03NK+XQpgHjmgyyJFMEtcvAo1FC46wf7/qJLbDE/5UY=&authSecret=0000019f02b34f2906ef0a64d5e20006'
requests.get(url)
hezi=requests.get(url).content
with open('唯一.html','wb') as f:
    f.write(hezi)
