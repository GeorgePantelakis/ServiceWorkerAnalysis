const puppeteer = require("puppeteer");
const scrape = require('website-scraper');

async function downloadSite(site){
    await scrape({
        urls: [
            site
        ],
        directory: './Downloaded_sites/' + site.split('/')[2] + '-' + site.split('/')[7],
        prettifyUrls: true,
        subdirectories: [
            {
                directory: 'img',
                extensions: ['.jpg', '.png', '.svg', '.webp', '.gif']
            },
            {
                directory: 'js',
                extensions: ['.js']
            },
            {
                directory: 'css',
                extensions: ['.css']
            },
            {
                directory: 'php',
                extensions: ['.php']
            },
            {
                directory: 'fonts',
                extensions: ['.woff', '.ttf', '.woff2', '.eot']
            }
        ]
    }).then(function (result) {
        // Outputs HTML 
        // console.log(result);
        console.log(site.split('/')[2] + " content succesfully downloaded.");
    }).catch(function (err) {
        console.log("Failed to download " + site.split('/')[7] + ".");
    });
}

let urlToScrape = [
    'https://web.archive.org/web/20180815003005if_/https://www.youtube.com/',
    'https://web.archive.org/web/20131014212210/http://stackoverflow.com/',
    'https://web.archive.org/web/20131020224056/http://www.foodnetwork.com/',
    'https://web.archive.org/web/20131021165347/http://www.imdb.com/',
    'https://web.archive.org/web/20150428170340/http://ubl.com/',
    'https://web.archive.org/web/20131001231045/http://www.bloomberg.com/',
    'https://web.archive.org/web/20131018071258/http://www.reference.com/',
    'https://web.archive.org/web/20131021205646/http://www.wikihow.com/Main-Page',
    'https://web.archive.org/web/20131021172452/http://www.nbcnews.com/',
    'https://web.archive.org/web/20131021004242/http://www.goodreads.com/'
]

describe("Just run the browser", () => {
    for(let i = 0; i < urlToScrape.length; i++){
        it("Should scrape a site", async function(){
            //open the browser and a new page
            const browser = await puppeteer.launch({
                headless: false,
                defaultViewport: {
                    width: 1500,
                    height: 1000
                },
                devtools: false
            });
            const pages = await browser.pages();
            const page = pages[0];

            page.setDefaultNavigationTimeout(150000);

            //add the puppeteer code
            await page.goto(urlToScrape[i], {waitUntil: 'load'});
            console.log(await page.url());
            await downloadSite(page.url());

            //close the browser
            await browser.close();
        })
    }
})