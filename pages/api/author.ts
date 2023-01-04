import puppeteer from 'puppeteer-core';
import edgeChromium from 'chrome-aws-lambda'

const LOCAL_CHROME_EXECUTABLE = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
export default async function handler(req, res) {
    const username: string = req.query.username;
    if(username == null || username == '') res.status(500).json({error: 'No username provided. Check docs at https://github.com/alombi/rh-api'});
    const baseURL = `https://routinehub.co/user/${username}`;

    const executablePath = await edgeChromium.executablePath || LOCAL_CHROME_EXECUTABLE
    const browser = await puppeteer.launch({
        executablePath,
        args: edgeChromium.args,
        headless: false,
    })
    const page = await browser.newPage();
    page.setUserAgent('Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    await page.goto(baseURL);
    const is404 = await checkForResults(page);
    if(is404){
        res.status(404).json({error: 'User not found'});
    }

    const subtitle = await page.evaluate(() => document.querySelector('.subtitle').textContent) as string;
    let avatar = await page.evaluate(()=> document.querySelector('.profile-picture img')?.getAttribute('src')) as string;
    if(avatar == undefined){
        avatar = 'No profile picture found.';
    }else{
        avatar = 'https' + avatar.split('https')[1];
    }
    const total_shortcuts = await page.evaluate(() => document.querySelectorAll('.stats > p')[0]?.textContent).then((e)=>e.replace('Shortcuts: ', '')) as string;
    const total_downloads = await page.evaluate(() => document.querySelectorAll('.stats > p')[1]?.textContent).then((e)=>e.replace('Downloads: ', '')) as string;
    let isMember: string | boolean = await page.evaluate(()=> document.querySelectorAll('.tag')[0]?.textContent) as string;
    if(isMember == 'Member'){
        isMember = true;
    }else{
        isMember = false;
    }
    let isMod: string | boolean = await page.evaluate(()=> document.querySelectorAll('.tag')[1]?.textContent) as string;
    if(isMod == 'Mod'){
        isMod = true;
    }else{
        isMod = false;
    }

    const contacts = {
        keybase: await page.evaluate(()=> document.querySelector('.fa-keybase')?.parentElement.parentElement.getAttribute('href')),
        twitter: await page.evaluate(()=> document.querySelector('.fa-twitter')?.parentElement.parentElement.getAttribute('href')),
        facebook: await page.evaluate(()=> document.querySelector('.fa-facebook-alien')?.parentElement.parentElement.getAttribute('href')),
        reddit : await page.evaluate(()=> document.querySelector('.fa-reddit-alien')?.parentElement.parentElement.getAttribute('href')),
        youtube: await page.evaluate(()=> document.querySelector('.fa-youtube')?.parentElement.parentElement.getAttribute('href')),
        github: await page.evaluate(()=> document.querySelector('.fa-github')?.parentElement.parentElement.getAttribute('href')),
        gitlab: await page.evaluate(()=> document.querySelector('.fa-gitlab')?.parentElement.parentElement.getAttribute('href')),
        website: await page.evaluate(()=> document.querySelector('.fa-globe')?.parentElement.parentElement.getAttribute('href')),
        email: await page.evaluate(()=> document.querySelector('.fa-envelope')?.parentElement.parentElement.getAttribute('href').replace('mailto:', ''))
    }
    

    await browser.close()
    res.status(200).json({
        username: username,
        avatar: avatar,
        subtitle: subtitle,
        stats:{
            total_shortcuts: Number(total_shortcuts),
            total_downloads: Number(total_downloads),
            downloads_average: Number(total_downloads) / Number(total_shortcuts)
        },
        isMember: isMember,
        isMod: isMod,
        contacts: contacts
    })

}

async function checkForResults(page){
    let notFoundString = await page.evaluate(()=> document.querySelector('h3')?.textContent) as string
    notFoundString = notFoundString.replace(/\n/g, '');
    if(notFoundString == 'Error: Profile not found'){
        return true;
    }else{
        return false;
    }
}