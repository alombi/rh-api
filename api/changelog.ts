import puppeteer from 'puppeteer';

async function checkForResults(page){
    let notFoundString = await page.waitForSelector('#content > div > div > div');
    notFoundString = await notFoundString?.evaluate((e) => e.innerText);
    if(notFoundString == 'No results found.'){
        return true;
    }else{
        return false;
    }
}

module.exports = async (req, res) => {
    const query: string = req.query.q;
    const baseURL: string = `https://routinehub.co/search/?q=${query}`;

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.setUserAgent('Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    await page.goto(baseURL);

    const hasNoResults = await checkForResults(page);
    if(hasNoResults){
        res.json({
            results: [],
            error: 'No results found.'
        })
    }
    // const results = await page.evaluate(() =>
    //     Array.from(document.querySelectorAll('a'),(e)=>({
    //         id: Number(e.querySelector('a')?.href)
    //     }))
    // )
    let container = await page.waitForSelector('#content > div > div');
    const results = await container?.evaluate((e) => Array.from(e.querySelectorAll('.column'), (el) => ({
        name:el.querySelector('strong')?.innerText,
        id: Number(el.querySelector('a')?.href.replace('https://routinehub.co/shortcut/', '').replace('/', '')),
        description: el.querySelector('small')?.innerText,
        downloads: Number(el.querySelectorAll('small')[1]?.innerText),
        hearts: Number(el.querySelectorAll('small')[2]?.innerText),
        link: el.querySelector('a')?.href,
        api_link: 'https://rh-api.alombi.xyz/shortcut?id=' + Number(el.querySelector('a')?.href.replace('https://routinehub.co/shortcut/', '').replace('/', '')),
        routinehub_api_link: `https://routinehub.co/api/v1/shortcuts/${Number(el.querySelector('a')?.href.replace('https://routinehub.co/shortcut/', '').replace('/', ''))}/versions/latest`
    })))
    const totalResults = results?.length;
    

    res.json({
        totalResults: totalResults,
        results:results
    })
}