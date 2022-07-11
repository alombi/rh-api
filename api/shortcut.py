import bs4, requests, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import random

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

def relatedByAuthor(username, name):
   url = f'https://routinehub.co/user/{username}'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   relatedName = str(soup.select('.shortcut-card')[0].select('strong')[0]).replace('<strong>', '').replace('</strong>', '')
   if relatedName != name:
      relatedId = str(soup.select('.shortcut-card')[0].parent['href']).replace('/shortcut/', '').replace('/', '')
   else:
      relatedName = str(soup.select('.shortcut-card')[1].select('strong')[0]).replace('<strong>', '').replace('</strong>', '')
      relatedId = str(soup.select('.shortcut-card')[1].parent['href']).replace('/shortcut/', '').replace('/', '')
   return (relatedName, relatedId)

def relatedByCategory(category, name):
   url = f'https://routinehub.co/category/{category}/'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   i = random.sample(range(1, 15), 1)[0]
   relatedName = str(soup.select('.shortcut-card')[i].select('strong')[0]).replace('<strong>', '').replace('</strong>', '')
   if relatedName != name:
      relatedId = str(soup.select('.shortcut-card')[i].parent['href']).replace('/shortcut/', '').replace('/', '')
   else:
      relatedName = str(soup.select('.shortcut-card')[i + 1].select('strong')[0]).replace('<strong>', '').replace('</strong>', '')
      relatedId = str(soup.select('.shortcut-card')[i + 1].parent['href']).replace('/shortcut/', '').replace('/', '')
   return (relatedName, relatedId)

class handler(BaseHTTPRequestHandler):
   def do_GET(self):
      parsed_path = urlparse(self.path)
      path = '?' + parsed_path.query
      try:
         wantsRelated = parse_qs(path[1:])["related"][0]
         if wantsRelated == "false":
            wantsRelated = False
         else:
            wantsRelated = True
      except:
         wantsRelated = False
      try:
         icon = parse_qs(path[1:])["icon"][0]
         if icon == "false":
            icon = False
         else:
            icon = True
      except:
         icon = False
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
         author = extract(soup, '#content > div > div > div.column.sidebar.is-2 > div.information > p:nth-child(1) > a > strong').replace('@', '')
         hearts = extract(soup, '#content > div > div > div.column.sidebar.is-2 > div.heart.has-text-centered')
         downloads = scrapeDownloads(soup)
         name = extract(soup, '#content > div > article > div > div > div > h3')
         description = extract(soup, '#content > div > article > div > div > div > h4')
         if len(soup.select('.information')[0].find('ul').find_all('li')) == 1:
            category_01 = str(soup.select('.information')[0].find('ul').find('li').find('a')['href']).replace('/category/', '').replace('/', '').capitalize()
            categories = [category_01]
         else:
            category_01 = str(soup.select('.information')[0].find('ul').find('li').find('a')['href']).replace('/category/', '').replace('/', '').capitalize()
            category_02 = str(soup.select('.information')[0].find('ul').find_all('li')[1].find('a')['href']).replace('/category/', '').replace('/', '').capitalize()
            categories = [category_01, category_02]
         data = {
         "id":RoutineHubID,
         "name":name,
         "description":description,
         "hearts":hearts,
         "downloads": downloads,
         "author": author,
         "categories": categories,
         }
         if wantsRelated:
            data["related"] = []
            # Related 01
            try:
               related_01 = relatedByAuthor(author, name)
            except:
               related_01 = (None, None)
            data["related"].append({ "name":related_01[0], "id":related_01[1] })
            # Related 02
            for category in categories:
               related_02 = relatedByCategory(category, name)
               data["related"].append(related_02)
  
         if icon:
            apiv1 = requests.get(f'https://routinehub.co/api/v1/shortcuts/{RoutineHubID}/versions/latest')
            apiv1 = apiv1.json()
            shortcutID = apiv1['URL'].split('/')[-1]
            icloudAPI = f'https://www.icloud.com/shortcuts/api/icons/{shortcutID}'
            iconReq = requests.get(icloudAPI)
            icon = ("data:" + 
            iconReq.headers['Content-Type'] + ";" + "base64," + base64.b64encode(iconReq.content).decode("utf-8"))
            icon = icon.replace('data:image;base64,', '')
            data["icon"] = icon
  
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(json.dumps(data).encode())
      return