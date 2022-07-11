const rp = require('request-promise');
const $ = require('cheerio');

module.exports = async (req, res) => {
   let q = req.query.q
   let url = "https://routinehub.co/search/?q=" + q
   rp(url)
      .then((html) => {
         if ($('#content > div > div > div > p', html).text().indexOf('No results found') != -1) {
            res.setHeader('Content-type', 'application/json')
            res.json({'results':[]})
         } else {
            let json = {
               'results': []
            }

            let n = $("#content > div > div", html)['0'].children.length;
            n = (n - 1) / 2
            for (let i = 0; i < n; i++) {
               console.log(i)
               var name = $(`#content > div > div > div:nth-child(${i + 1}) > a > div > div > div > div > div > p > strong`, html).text();
               var description = $(`#content > div > div > div:nth-child(${i + 1}) > a > div > div > div > div > div > p > small`, html).text();
               var hearts = $(`#content > div > div > div:nth-child(${i + 1}) > a > div > div > div > div > nav > div.level-right > span:nth-child(1) > small`, html).text();
               var downloads = $(`#content > div > div > div:nth-child(${i + 1}) > a > div > div > div > div > nav > div.level-right > span:nth-child(2) > small`, html).text();
               var RHid = $(`#content > div > div > div:nth-child(${i + 1}) > a`, html)['0'].attribs.href.replace('/shortcut/', '').replace('/', '');
               var link = 'https://routinehub.co' + $(`#content > div > div > div:nth-child(${i + 1}) > a`, html)['0'].attribs.href;
               var api_link = 'https://rh-api.alombi.xyz/shortcut?id=' + RHid
               var obj = {
                  'id': Number(RHid),
                  'name': name,
                  'description': description,
                  'hearts': Number(hearts),
                  'downloads': Number(downloads),
                  'link': link,
                  'api_link': api_link
               }
               json.results.push(obj)
            }

            res.setHeader('Content-type', 'application/json')
            res.json(json)
         }
      })
      .catch((err)=>{
         res.setHeader('Content-type', 'application/json')
         console.log(err)
         if (!q) {
            res.json({ 'Error': 'Required parameter was not given or was incorrect. Check docs at https://rh-api.alombi.xyz' })
         } else {
            res.json({'Error':'Something went wrong. Check docs at https://rh-api.alombi.xyz'})
         }
      })
}