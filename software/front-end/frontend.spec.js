const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000'); // Change the URL to your frontend URL

  // Test Capture Button
  await page.click('button#capture'); // Change the selector to match your button
  const response = await page.waitForResponse(response => response.url() === '/api/capture' && response.status() === 200);
  console.assert(response.ok(), 'Capture button did not trigger the correct POST request');

  // Test Shutdown Button
  await page.click('button#shutdown'); // Change the selector to match your button
  const shutdownResponse = await page.waitForResponse(response => response.url() === '/api/shutdown' && response.status() === 200);
  console.assert(shutdownResponse.ok(), 'Shutdown button did not trigger the correct POST request');

  await browser.close();
})();
