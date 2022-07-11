import bs4, requests
from http.server import BaseHTTPRequestHandler
import json

def scrapeText():
   url = f'https://routinehub.co'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   return soup

def extract(soup, selector):
  elems = soup.select(selector)
  return elems


class handler(BaseHTTPRequestHandler):
   def do_GET(self):
      soup = scrapeText()
      trending = {
         'trending':[],
         'new':[],
         'recently-updated':[]
      }
      i = 1
      j = 1
      while j < 4:
         i = 1
         if j == 1:
            param = 'trending'
         elif j == 2:
            param = 'new'
         elif j == 3:
            param = 'recently-updated'
         while i < 7:
            elem = extract(soup, f'#shortcut-lists > div:nth-child(2) > div.{param}.home-list > div > div:nth-child({i})')
            name = str(elem[0].select('a > div > div > div > div > div > p > strong')).replace('[<strong>', '').replace('</strong>]', '')
            print(name)
            desc = str(elem[0].select(f'#shortcut-lists > div:nth-child(2) > div.{param}.home-list > div > div:nth-child({i}) > a > div > div > div > div > div > p > small')).replace('[<small>', '').replace('</small>]', '')
            downloads = int(elem[0].select(f'#shortcut-lists > div:nth-child(2) > div.{param}.home-list > div > div:nth-child({i}) > a > div > div > div > div > nav > div.level-right > span:nth-child(1) > small')[0].get_text())
            hearts = int(elem[0].select(f'#shortcut-lists > div:nth-child(2) > div.{param}.home-list > div > div:nth-child({i}) > a > div > div > div > div > nav > div.level-right > span:nth-child(2) > small')[0].get_text())
            link = 'https://routinehub.co' + elem[0].select(f'#shortcut-lists > div:nth-child(2) > div.{param}.home-list > div > div:nth-child({i}) > a')[0]['href']
            RHid = str(elem[0].select(f'#shortcut-lists > div:nth-child(2) > div.{param}.home-list > div > div:nth-child({i}) > a')[0]['href']).replace('/shortcut/', '').replace('/', '')
            api_link = 'https://rh-api.alombi.xyz/shortcut?id=' + RHid
            #
            # Needs to convert downloads and hearts in NUMBERS
            #
            shortcut = {
               'name':name,
               'id':int(RHid),
               'description':desc,
               'downloads':downloads,
               'hearts':hearts,
               'link':link,
               'api_link':api_link
            }
            i = i + 1
            trending[param].append(shortcut)
         j = j + 1      

      #data = str(trending).replace('\'', '\"')
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(json.dumps(trending).encode())
      return