import puppeteer from 'puppeteer-core';
import edgeChromium from 'chrome-aws-lambda'

async function checkForResults(page){
    let notFoundString = await page.waitForSelector('#content > div > div > div');
    notFoundString = await notFoundString?.evaluate((e) => e.innerText);
    if(notFoundString == 'No results found.'){
        return true;
    }else{
        return false;
    }
}
const LOCAL_CHROME_EXECUTABLE = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
export default async function handler(req, res) {
    const executablePath = await edgeChromium.executablePath || LOCAL_CHROME_EXECUTABLE
    const query: string = req.query.q;
    const baseURL: string = `https://routinehub.co/search/?q=${query}`;

    const browser = await puppeteer.launch({
        executablePath,
        args: edgeChromium.args,
        headless: false,
    })
    const page = await browser.newPage();
    page.setUserAgent('Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    await page.goto(baseURL);

    const hasNoResults = await checkForResults(page);
    if(hasNoResults){
        res.status(500).son({
            results: [],
            error: 'No results found.'
        })
    }
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
    

    res.status(200).json({
        totalResults: totalResults,
        results:results
    })
}
