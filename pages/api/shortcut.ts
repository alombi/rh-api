import puppeteer from 'puppeteer-core';
import edgeChromium from 'chrome-aws-lambda'

const LOCAL_CHROME_EXECUTABLE = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
export default async function handler(req, res) {
    const id = Number(req.query.id);
    if(id == null || id == 0) res.status(500).json({error: 'No ID provided. Check docs at https://github.com/alombi/rh-api'});
    const baseURL: string = `https://routinehub.co/shortcut/${id}/`

    const executablePath = await edgeChromium.executablePath || LOCAL_CHROME_EXECUTABLE
    const browser = await puppeteer.launch({
        executablePath,
        args: edgeChromium.args,
        headless: false,
    })
    const page = await browser.newPage();
    page.setUserAgent('Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    await page.goto(baseURL);

    const shortcutName = await page.evaluate(() => document.querySelectorAll('h3')[0].textContent) as string;
    const description = await page.evaluate(() => document.querySelectorAll('h4')[0].textContent) as string;
    const hearts = await page.evaluate(() => document.querySelector('.heart-count')?.textContent) as string;
    const downloads = await page.evaluate(() => document.querySelectorAll('.information > p')[4]?.textContent).then((e)=>e.replace('Downloads: ', '')) as string;
    const author = await page.evaluate(() => document.querySelectorAll('.information > p')[0]?.textContent).then((e)=>e.replace('Author:\n@', '').replace('\n', '')) as string;
    const authorURL = await page.evaluate(() => document.querySelectorAll('.information > p')[0].querySelector('a')?.href) as string;
    const latest_version = await page.evaluate(() => document.querySelectorAll('.information > p')[1]?.textContent).then((e)=>e.replace('Version: ', '')) as string;
    const updated = await page.evaluate(() => document.querySelectorAll('.information > p')[3]?.textContent).then((e)=>e.replace('Updated: ', '')) as string;
    const iOS_version = await page.evaluate(() => document.querySelectorAll('.information > p')[2]?.textContent).then((e)=>e.replace('iOS: ', '')) as string;
    const categories = await page.evaluate(()=>
        Array.from(document.querySelectorAll('.information > ul')[0].querySelectorAll('li'),(e)=>(e.innerText))
    ) as string[];
    const download_link = await page.evaluate(() => document.querySelector('.actions')?.querySelector('a')?.href) as string;



    await browser.close()
    res.status(200).json({
        id: id,
        name: shortcutName,
        description: description,
        hearts: Number(hearts),
        downloads: Number(downloads),
        author: {
            username: author,
            page_link: authorURL,
            api_link: `https://rh-api.alombi.xyz/author?username=${author}`
        },
        latest_version: {
            version: latest_version,
            updated: updated
        },
        iOS: iOS_version,
        categories: categories,
        download_link: download_link
    })
}