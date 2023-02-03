const fetch = require('node-fetch');
const fs = require('fs');

let UUID = process.env.UUID;
let SERVER_URL = process.env.SERVER_URL || 'http://host.docker.internal:8000';

// Request performance object entrypoint
let url = `${SERVER_URL}/api/request/${UUID}/performance`

if (process.env.ENABLE_LIGHTHOUSE == 0) {
	console.log('ENABLE_LIGHTHOUSE == 0, disabling lighthouse report');
	return;
}

async function runPerformanceTask () {

	while(true) {
		// Fetch url from docker
		try {
			// Fetch next performance object to evaluate
			const response = await fetch(url);
			const data = await response.json();

			if (data && data.performance && data.performance.url) {

				console.log(`Running test on ${data.performance.url}`);
				// Send url to googleapis
				const report = await fetch(`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${data.performance.url}&category=accessibility&category=best-practices&category=performance&category=pwa&category=seo`);
				const json = await report.json();

				// Save received report as json (TODO: delete)
				// fs.writeFile(`report-${data.performance.pk}.json`, JSON.stringify(json.lighthouseResult, null, 2), (err) => {
				// 	if (err) {
				// 		throw err;
				// 	}
				// 	console.log("File has been created");
				// });

				// Send report to server
				const reportResponse = await fetch(`${SERVER_URL}/api/report/${UUID}/performance/${data.performance.pk}`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(json.lighthouseResult)
				});
				console.log("Report has been forwarded");

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