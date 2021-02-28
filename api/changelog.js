const rp = require('request-promise');
const $ = require('cheerio');

module.exports = async (req, res) =>{
   let id = req.query.id;
   let url = `https://routinehub.co/shortcut/${id}/changelog`;
   rp(url)
      .then((html)=>{
         let versions = $('#content > div > div.versions > article', html).length;
         let name = $('#content > div > div.heading > h4', html).text();
         let json = {
            'id':id,
            'name':name,
            'updates':versions,
            'versions':[]
         }
         for(var i = versions; i > 0; i--){
            let version = $(`#content > div > div.versions > article:nth-child(${i}) > div > div > p > strong`, html).text();
            let release_date = $(`#content > div > div.versions > article:nth-child(${i}) > div > div > p > small:first-of-type`, html).text();
            let iOS = $(`#content > div > div.versions > article:nth-child(${i}) > div > div > p > small:last-of-type`, html).text();
            let downloads = $(`#content > div > div.versions > article:nth-child(${i}) > div > div > p > em`, html).text()

            let htmlFixed = $(`#content > div > div.versions > article:nth-child(${i}) > div > div > p`, html).html().split('<br>');
            _ = htmlFixed.pop()
            _ = htmlFixed.pop()
            _ = htmlFixed.shift()
            _ = htmlFixed.shift()
            let release_notes = htmlFixed.join('\n')
            
            var versionJSON = {
               'version':version,
               'release_date':release_date,
               'iOS':iOS,
               'release_notes':release_notes,
               'downloads':downloads
            }
            json.versions.push(versionJSON)
         }
         json.versions.reverse()
         res.setHeader('Content-type', 'application/json')
         res.json(json)
      })
      .catch((err)=>{
         res.setHeader('Content-type', 'application/json')
         console.log(err)
         res.json('Error')
      })
}