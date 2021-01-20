import bs4, requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def scrape(id, selector):
  url = f'https://routinehub.co/shortcut/{id}/changelog'
  req = requests.get(url)
  req.raise_for_status()
  soup = bs4.BeautifulSoup(req.text, 'html.parser')
  elems = soup.select(selector)
  return elems


class handler(BaseHTTPRequestHandler):
  def do_GET(self):
    parsed_path = urlparse(self.path)
    path = '?' + parsed_path.query
    RoutineHubID =  parse_qs(path[1:])["id"][0]
    text = scrape(RoutineHubID, '#content > div > div.versions')

    data = {
      "id":RoutineHubID
    }
    elems = scrape(RoutineHubID, '#content > div > div.heading > h4')
    res = elems[0].text.strip()
    data["name"] = res
    # Get number of versions
    number_of_versions = 0
    for word in str(text).split():
      if word == '<article':
        number_of_versions = number_of_versions + 1
    data["updates"] = number_of_versions
    child = 1
    i = number_of_versions
    versions = {
      "versions":[]
    }
    while i != 0:
      text = scrape(RoutineHubID, f'#content > div > div.versions > article:nth-child({str(child)})')
      version = str(text).split('\n')[4].split('</strong>')[0].replace('<strong>', '')
      versionData = {
        "version":version
      }
      release_date = str(text).split('\n')[4].split('<small>')[1].replace('</small>', '')
      versionData["release_date"] = release_date
      iOS = str(text).split('\n')[6].replace('</small>', '').replace('<small>', '')
      versionData["iOS"] = iOS
      release_notes = str(text).split('<br/>')[2].split('<br/>')[0]
      versionData["release_notes"] = release_notes
      downloads = str(text).split('\n')[10].replace('</em>', '').replace('<em>', '')
      versionData["downloads"] = downloads

      versions["versions"].append(versionData)

      child = child + 1
      i = i -1 
    data["versions"] = versions
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(str(data).encode())
    return
