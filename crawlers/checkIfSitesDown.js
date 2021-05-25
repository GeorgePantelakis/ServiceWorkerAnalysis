const puppeteer = require('puppeteer');
const fs = require('fs');
const color = require('colors');

let browser;
let sites = [];
let unreachableSites = [];

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function readSites(){
    let input_file = process.argv[2].substr(1,process.argv[2].length);

    rawData = fs.readFileSync(input_file, {encoding: 'ascii'});
    rawDataList = rawData.split('\n');

    if(rawDataList[rawDataList.length - 1] === '')
        rawDataList.pop();

    for(let j = 0; j < rawDataList.length; j++){
        data = rawDataList[j];
        if(data === undefined)continue;
        if(data.search("http") !== -1)sites.push(data);
        else if(data.search("www") !== -1)sites.push("http://" + data);
        else sites.push("http://www." + data);
    }

    if(sites.length > 0)
        console.log("File " + input_file + " was successfully read.");
}

function writeResults(){
    try{
        var file = fs.createWriteStream('results/unreachableSites.txt');
        for(writeLoop = 0; writeLoop < unreachableSites.length; writeLoop++){
            file.write(unreachableSites[writeLoop] + "\n");
        }
        file.end();
        console.log("unreachableSites.txt was successfully created!\n");
    }catch(err){
        console.log("\n\n");
        console.log("Unrechable Sites:\n");
        console.log(unrechableSites);
    }
}

async function Main(){
    browser = await puppeteer.launch({
        headless: false,
        devtools: true,
        defaultViewport:{
            height: 1200,
            width: 1200,
            isMobile: false
        },
        //executablePath: "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        args: [
            //"--proxy-server=http://127.0.0.1:8080",
            "--ignore-certificate-errors",
            "--headless"
        ]
    });

    let pages =  await browser.pages();
    const page = pages[0];

    await readSites();
    
    let total = sites.length

    for(item in sites){
        console.log('(' + (parseInt(item, 10) + 1) + '/' + total + ') Checking url ' + sites[item]);
        try {
            await page.goto(sites[item], {waitUntil: 'load', timeout: 0}); 
            console.log(`responded`.green);   
        } catch(e) {
            unreachableSites.push(sites[item])
            console.log(`not responded`.red);
        }
    }

    await writeResults();

    browser.close()
}

Main()