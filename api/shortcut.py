import bs4, requests, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

def scrape(id):
   url = f'https://routinehub.co/shortcut/{id}/'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   return soup

def extract(soup, selector):
   elems = soup.select(selector)
   res = elems[0].text.strip()
   return res

def scrapeDownloads(soup):
   res = soup.select('.information > p ')[0].select('p')[3].text
   res = res.split('Downloads: ')[1]
   return res


class handler(BaseHTTPRequestHandler):
  def do_GET(self):
      parsed_path = urlparse(self.path)
      path = '?' + parsed_path.query
      try:
         RoutineHubID =  parse_qs(path[1:])["id"][0]
         isValid = True
         soup = scrape(RoutineHubID)
         if 'Error: Shortcut not found' in str(soup):
            isValid = False
            data = 'The provided id does not exist or it\'s invalid.'
      except:
         isValid = False
         data = 'Required parameter was not given or was incorrect. Check docs at https://rh-api.alombi.xyz'

      if isValid:
         hearts = extract(soup, '#content > div > div > div.column.sidebar.is-2 > div.heart.has-text-centered')
         downloads = scrapeDownloads(soup)
         name = extract(soup, '#content > div > article > div > div > div > h3')
         subtitle = extract(soup, '#content > div > article > div > div > div > h4')
         apiv1 = requests.get('https://routinehub.co/api/v1/shortcuts/5015/versions/latest')
         apiv1 = apiv1.json()
         shortcutID = apiv1['URL'].split('/')[-1]
         icloudAPI = f'https://www.icloud.com/shortcuts/api/icons/{shortcutID}'
         iconReq = requests.get(icloudAPI)
         icon = ("data:" + 
         iconReq.headers['Content-Type'] + ";" + "base64," + base64.b64encode(iconReq.content).decode("utf-8"))
         icon = icon.replace('data:image;base64,', '')
         data = {
            "id":RoutineHubID,
            "name":name,
            "subtitle":subtitle,
            "hearts":hearts,
            "downloads":downloads,
            'icon':icon
         }
         #data = str(data).replace('\'', '\"')

      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(json.dumps(data).encode())
      return
