// const fetch = require('node-fetch');
// const fs = require('fs');

import fetch from 'node-fetch';
import fs from 'fs';

// const lighthouse = require('lighthouse');
// const googleLAuncher = require('chrome-launcher');
// Load lighthouse and chrome-launcher to setup lighthouse locally
import lighthouse from 'lighthouse';
import chromeLauncher from 'chrome-launcher';

let UUID = process.env.UUID;
let SERVER_URL = process.env.SERVER_URL || 'http://host.docker.internal:8000';
const USER_AGENT = 'FromEdwinBot node lighthouse';

// Request performance object entrypoint
let url = `${SERVER_URL}/api/request/${UUID}/performance`

if (process.env.DISABLE_LIGHTHOUSE == 1) {
	console.log('❌  DISABLE_LIGHTHOUSE == 1, disabling lighthouse report');
	process.exit(1);
}

// Constant copied from https://github.com/GoogleChrome/lighthouse/blob/main/core/config/constants.js
const DESKTOP_EMULATION_METRICS = {
  mobile: false,
  width: 1350,
  height: 940,
  deviceScaleFactor: 1,
  disabled: false,
};

const MOTOGPOWER_EMULATION_METRICS = {
  mobile: true,
  width: 412,
  height: 823,
  // This value has some interesting ramifications for image-size-responsive, see:
  // https://github.com/GoogleChrome/lighthouse/issues/10741#issuecomment-626903508
  deviceScaleFactor: 1.75,
  disabled: false,
};

const screenEmulationMetrics = {
  mobile: MOTOGPOWER_EMULATION_METRICS,
  desktop: DESKTOP_EMULATION_METRICS,
};

const MOTOG4_USERAGENT = 'Mozilla/5.0 (Linux; Android 11; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 fromedwin'; // eslint-disable-line max-len
const DESKTOP_USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 fromedwin'; // eslint-disable-line max-len

/**
 * Start infinite to start generating lighthouse reports
 **/
async function runPerformanceTask () {

	while(true) {
		// Fetch url from docker
		try {
			// Fetch next performance object to evaluate
			const response = await fetch(url, {
				headers: {
					'User-Agent': USER_AGENT,
				}
			});
			const data = await response.json();

			if (data && data.performance && data.performance.url) {

				console.log(`Running test on ${data.performance.url}`);

				// Start Chrome process
				const chrome = await chromeLauncher.launch({
					ignoreDefaultFlags: true,
					chromeFlags: [
							'--headless',
							'--no-sandbox',
							'--disable-dev-shm-usage',
							'--allow-pre-commit-input',
							'--in-process-gpu',
						]
					}); //  '--disable-gpu', '--disable-setuid-sandbox'

				// Running Lighthouse by custom options
				const options = {
					logLevel: 'info', 
					output: 'json', 
					port: chrome.port,
					formFactor: 'desktop', // 'desktop' or 'mobile'
					screenEmulation: screenEmulationMetrics.desktop,
					emulatedUserAgent: DESKTOP_USERAGENT, //MOTOG4_USERAGENT,
					skipAudits: [
					    // Skip the h2 audit so it doesn't lie to us. See https://github.com/GoogleChrome/lighthouse/issues/6539
					    'uses-http2',
					    // There are always bf-cache failures when testing in headless. Reenable when headless can give us realistic bf-cache insights.
					    'bf-cache',
				    ],
				};
				const runnerResult = await lighthouse(data.performance.url, options);

				// Send report to server
				const reportResponse = await fetch(`${SERVER_URL}/api/report/${UUID}/performance/${data.performance.pk}`, {
					method: 'POST',
					headers: {
						'User-Agent': USER_AGENT,
						'Content-Type': 'application/json'
					},
					body: runnerResult.report
				});
				console.log("Report has been forwarded");
				await chrome.kill();

				// Wait 1 seconds before next request
				await new Promise(resolve => setTimeout(resolve, 1000));
			} else {
				// Wait 5 seconds before next request
				await new Promise(resolve => setTimeout(resolve, 5000));
			}
		} catch (error) {
			console.error(error);
			console.log('Wait for 10 seconds');
			// Wait 5 seconds before next request
			await new Promise(resolve => setTimeout(resolve, 10000));
		}
	}
}

runPerformanceTask();