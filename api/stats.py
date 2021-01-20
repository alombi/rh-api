import bs4, requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

def scrape(id, selector):
   url = f'https://routinehub.co/shortcut/{id}/'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   elems = soup.select(selector)
   res = elems[0].text.strip()
   return res

def scrapeDownloads(id):
   url = f'https://routinehub.co/shortcut/{id}/'
   req = requests.get(url)
   req.raise_for_status()
   soup = bs4.BeautifulSoup(req.text, 'html.parser')
   res = soup.select('.information > p ')[0].select('p')[3].text
   res = res.split('Downloads: ')[1]
   return res


class handler(BaseHTTPRequestHandler):
  def do_GET(self):
      parsed_path = urlparse(self.path)
      path = '?' + parsed_path.query
      RoutineHubID =  parse_qs(path[1:])["id"][0]
      hearts = scrape(RoutineHubID, '#content > div > div > div.column.sidebar.is-2 > div.heart.has-text-centered')
      downloads = scrapeDownloads(RoutineHubID)
      data = {
         'id':RoutineHubID,
         'hearts':hearts,
         'downloads':downloads
      }
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(str(data).encode())
      return
