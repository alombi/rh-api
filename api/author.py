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

def scrapePage(username, page):
   url = f'https://routinehub.co/user/{username}?page={page}'
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
         try:
            avatar = extractAttribute(soup, '#content > div > div > div.column.sidebar.is-2 > figure > img', 'src')
         except:
            avatar = None
         try:
            bio = extractText(soup, '#content > div > div > div.column.details > div.is-hidden-mobile > p')
         except:
            bio =  None
         totalAuthored = int(extractText(soup, '#content > div > div > div.column.sidebar.is-2 > div.stats > p:nth-child(1)').replace('Shortcuts: ', ''))
         total_hearts = 0
         pages = soup.find_all('ul', class_='pagination-list')
         if pages == []:
            # Just one page
            totalAuthoredHTML = scrapeElems(RoutineHubAuthor, '#content > div > div > div.column.details > div.authored > div')
            totalAuthoredHTML = totalAuthoredHTML.select('.shortcut-card')
            index = len(totalAuthoredHTML)
            while index != 0:
               total_hearts = total_hearts + int(extractText(soup, f'#content > div > div > div.column.details > div.authored > div > div:nth-child({index}) > a > div > div > div > div > nav > div.level-right > span:nth-child(2)'))
               index = index - 1
         else:
            # More pages
            pages = len(str(pages[0]).replace('<ul class="pagination-list">', '').replace('</ul>', '').split('<li>')) - 1
            total_hearts = 0
            while pages > 0:
               soup_alt = scrapePage(RoutineHubAuthor, pages)
               totalAuthoredHTML = soup_alt.select('.shortcut-card')
               index = len(totalAuthoredHTML)
               while index != 0:
                  total_hearts = total_hearts + int(extractText(soup_alt, f'#content > div > div > div.column.details > div.authored > div > div:nth-child({index}) > a > div > div > div > div > nav > div.level-right > span:nth-child(2)'))
                  index = index - 1
               pages = pages -1
            print(total_hearts)
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
            'total_hearts':total_hearts,
            'hearts_average':hearts_average,
            'downloads_average':downloads_average
         }
         #data = str(data).replace('\'', '\"')
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps(data).encode())
      return