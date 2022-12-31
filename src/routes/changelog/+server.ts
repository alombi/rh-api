import { json } from '@sveltejs/kit';
import puppeteer from 'puppeteer';

export async function GET({url, setHeaders}){
    const id = Number(url.searchParams.get('id'));
    const baseURL: string = `https://routinehub.co/shortcut/${id}/changelog`;
    if(id == null || id == 0) return json({error: 'No ID provided.'});

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.setUserAgent('Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    //page.setUserAgent('DuckDuckBot')
    await page.goto(baseURL);

    const shortcutName = await page.evaluate(() => document.querySelectorAll('h4')[0].textContent) as string;
    const toalUpdates = await page.evaluate(() => Array.from(document.querySelectorAll('article.media')).length);
    const versions = await page.evaluate(() => 
        Array.from(document.querySelectorAll('article.media'),(e)=>({
            version: e.querySelector('strong')?.innerText,
            download_link: e.querySelector('a')?.href,
            release_date:e.querySelectorAll('small')[0]?.innerText,
            iOS: Number(e.querySelectorAll('small')[1]?.innerText.replace('iOS ', '')),
            changes: e.querySelector('p')?.innerHTML.split('</small>\n<br>\n')[2].split('\n<br><br>\n<em>')[0],
            downloads: Number(e.querySelector('em')?.innerText.replace(' downloads', '')),
        }))
    );

    await browser.close()

    setHeaders({
        "Content-type": "application/json;charset=UTF-8",
    })
    return json({
        id: id,
        name: shortcutName,
        toalUpdates: toalUpdates,
        versions:versions
    });
}