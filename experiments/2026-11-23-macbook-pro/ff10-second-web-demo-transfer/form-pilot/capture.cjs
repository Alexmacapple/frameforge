const {chromium}=require('/Users/alex/.local/share/shipguard-runtime/node_modules/playwright');
const path=require('path'),fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1920,height:1080},recordVideo:{dir:path.join(__dirname,'media'),size:{width:1920,height:1080}}});
 const page=await context.newPage();
 await page.goto('file://'+path.join(__dirname,'form.html'));
 await page.waitForTimeout(1200);
 await page.getByLabel('Votre nom').fill('Camille Martin');
 await page.waitForTimeout(3400);
 await page.getByLabel('Votre adresse électronique').fill('camille@example.test');
 await page.waitForTimeout(3700);
 await page.getByRole('button',{name:'Envoyer la demande'}).click();
 await page.getByRole('status').getByText('Demande enregistrée pour Camille Martin.').waitFor();
 await page.waitForTimeout(5600);
 console.log(JSON.stringify({name:await page.locator('#name').inputValue(),email:await page.locator('#email').inputValue(),confirmation:await page.locator('#result').innerText(),video:await page.video().path()}));
 await context.close();await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
