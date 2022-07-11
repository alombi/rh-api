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

def getSocial(soup):
   try:
      keybase = soup.find_all('i', class_='fa-keybase')[0].parent.parent['href']
   except:
      keybase = None
   try:
      twitter = soup.find_all('i', class_='fa-twitter')[0].parent.parent['href']
   except:
      twitter = None
   try:
      facebook = soup.find_all('i', class_='fa-facebook-alien')[0].parent.parent['href']
   except:
      facebook = None
   try:
      reddit = soup.find_all('i', class_='fa-reddit-alien')[0].parent.parent['href']
   except:
      reddit = None
   try:
      youtube = soup.find_all('i', class_='fa-youtube')[0].parent.parent['href']
   except:
      youtube = None
   try:
      github = soup.find_all('i', class_='fa-github')[0].parent.parent['href']
   except:
      github = None
   try:
      gitlab = soup.find_all('i', class_='fa-gitlab')[0].parent.parent['href']
   except:
      gitlab = None
   try:
      website = soup.find_all('i', class_='fa-globe')[0].parent.parent['href']
   except:
      website = None
   contacts = {
      'keybase':keybase,
      'twitter':twitter,
      'facebook':facebook,
      'reddit':reddit,
      'youtube':youtube,
      'github':github,
      'gitlab':gitlab,
      'website':website
   }
   return contacts   


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
            data = {'Error':'The provided username does not exist or it\'s invalid.'}
      except:
         isValid = False
         data = {'Error':'Required parameter was not given or was incorrect. Check docs at https://rh-api.alombi.xyz'}
      
      if isValid:
         try:
            avatar = extractAttribute(soup, '#content > div > div > div.column.sidebar.is-2 > figure > img', 'src')
         except:
            avatar = None
         try:
            bio = extractText(soup, '#content > div > div > div.column.details > div.is-hidden-mobile > p')
         except:
            bio =  None
         if soup.find_all('span', class_='tag is-primary') != []:
            member = True
         else:
            member = False
         if soup.find_all('span', class_='tag is-dark') != []:
            mod = True
         else:
            mod = False
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
               index = len(totalAuthoredHTML) - 1
               while index != 0:
                  total_hearts = total_hearts + int(extractText(soup_alt, f'#content > div > div > div.column.details > div.authored > div > div:nth-child({index}) > a > div > div > div > div > nav > div.level-right > span:nth-child(2)'))
                  index = index - 1
               pages = pages -1
         # Calculating pinned shortcut
         if'Pinned' in str(soup):
            total_hearts = total_hearts + int(extractText(soup, '#content > div > div > div.column.details > div.pinned > a > div > div > div > div > nav > div.level-right > span:nth-child(2)'))
            totalAuthored = totalAuthored + 1

         totalDownloads = extractText(soup, '#content > div > div > div.column.sidebar.is-2 > div.stats > p:nth-child(2)')
         totalDownloads = totalDownloads.split('Downloads: ')[1]
         downloads_average =round(int(totalDownloads) / int(totalAuthored), 2)
         hearts_average = round(int(total_hearts) / int(totalAuthored), 2)
         contacts = getSocial(soup)
         data = {
            'username':RoutineHubAuthor,
            'avatar':avatar,
            'bio':bio,
            'total_shortcuts':int(totalAuthored),
            'total_downloads':int(totalDownloads),
            'total_hearts':total_hearts,
            'hearts_average':hearts_average,
            'downloads_average':downloads_average,
            'contacts':contacts,
            'isMember':member,
            'isMod':mod
         }
      #data = str(data).replace('\'', '\"')
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps(data).encode())
      return