import puppeteer from 'puppeteer-core';
import edgeChromium from 'chrome-aws-lambda'

const LOCAL_CHROME_EXECUTABLE = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
export default async function handler(req, res) {
    const id = Number(req.query.id);
    if(id == null || id == 0) res.status(500).json({error: 'No ID provided.'});
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


    await browser.close()
    res.status(200).json({
        id: id,
        name: shortcutName,
        description: description
    })
}