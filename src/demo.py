import requests

# r = requests.get('https://s.taobao.com/api?\
#                  _input_charset=utf-8&\
#                  ajax=true&\
#                  bcoffset=-1&\
#                  ie=utf8&\
#                  initiative_id=staobaoz_20180423&\
#                  js=1&\
#                  m=customized&\
#                  q=搜狗旅行翻译宝&\
#                  s=36&\
#                  source=suggest&\
#                  stats_click=search_radio_all:1', 
#                  timeout=10, 
#                  headers={'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'})
r = requests.get('https://s.taobao.com/api?_ksTS=1524422800428_208&callback=jsonp209&ajax=true&m=customized&stats_click=search_radio_all:1&_input_charset=utf-8&bcoffset=-1&js=1&suggest=history_1&source=suggest&suggest_query=&q=搜狗旅行宝翻译机&s=36&initiative_id=staobaoz_20180423&imgfile=&wq=&ie=utf8&rn=419b5bdbaedc9c177281e02539a33c9a',
                 timeout=10, 
                 headers={'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'})
print(r.json())