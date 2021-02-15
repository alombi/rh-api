import bs4, requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

def scrapeText(username):
   url = f'https://routinehub.co/user/{username}'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   return soup

def extractText(soup, selector):
   elems = soup.select(selector)
   res = elems[0].text.strip()
   return res

def extractAttribute(soup, selector, attribute):
   elems = soup.select(selector)
   res = elems[0][attribute]
   return res

def scrapeElems(username, selector):
  url = f'https://routinehub.co/user/{username}'
  req = requests.get(url)
  req.raise_for_status()
  soup = bs4.BeautifulSoup(req.text, 'html.parser')
  return soup

class handler(BaseHTTPRequestHandler):
  def do_GET(self):
      parsed_path = urlparse(self.path)
      path = '?' + parsed_path.query
      try:
         RoutineHubAuthor =  parse_qs(path[1:])["username"][0]
         isValid = True
         soup = scrapeText(RoutineHubAuthor)
         if 'Error: Profile not found' in str(soup):
            isValid = False
            data = 'The provided username does not exist or it\'s invalid.'
      except:
         isValid = False
         data = 'Required parameter was not given or was incorrect. Check docs at https://rh-api.alombi.xyz'
      
      if isValid:
         avatar = extractAttribute(soup, '#content > div > div > div.column.sidebar.is-2 > figure > img', 'src')
         try:
            bio = extractText(soup, '#content > div > div > div.column.details > div.is-hidden-mobile > p')
         except:
            bio =  None
         totalAuthored = int(extractText(soup, '#content > div > div > div.column.sidebar.is-2 > div.stats > p:nth-child(1)').replace('Shortcuts: ', ''))
         total_hearts = 0
         totalDownloads = extractText(soup, '#content > div > div > div.column.sidebar.is-2 > div.stats > p:nth-child(2)')
         totalDownloads = totalDownloads.split('Downloads: ')[1]
         downloads_average =round(int(totalDownloads) / int(totalAuthored), 2)
         hearts_average = round(int(total_hearts) / int(totalAuthored), 2)
         data = {
            'username':RoutineHubAuthor,
            'avatar':avatar,
            'bio':bio,
            'total_shortcuts':totalAuthored,
            'total_downloads':totalDownloads,
            #'total_hearts':total_hearts,
            #'hearts_average':hearts_average,
            'downloads_average':downloads_average
         }
         #data = str(data).replace('\'', '\"')
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps(data).encode())
      return