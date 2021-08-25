
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
<!---
## [Unreleased] - yyyy-mm-dd

### ✨ Feature – for new features
### 🛠 Improvements – for general improvements
### 🚨 Changed – for changes in existing functionality
### ⚠️ Deprecated – for soon-to-be removed features
### 📚 Documentation – for documentation update
### 🗑 Removed – for removed features
### 🐛 Bug Fixes – for any bug fixes
### 🔒 Security – in case of vulnerabilities
### 🏗 Chore – for tidying code

See for sample https://raw.githubusercontent.com/favoloso/conventional-changelog-emoji/master/CHANGELOG.md
-->
## [0.2.0] - yyyy-mm-dd
### ✨ Feature
- Provide run scripts to automate some configuration [#1](https://github.com/fromedwin/monitor-client/issues/1)
- Fetch prometheus and alerts configuration files on start [#2](https://github.com/fromedwin/monitor-client/issues/2)

## [0.1.0] - 2021-08-11
### ✨ Feature
- Prometheus use local configuration to define jobs and start monitoring
- Nginx generate SSL certificate with local stored domain
- Report to hard coded alertmanager url
- Access is protected using web auth mechanism
- Using docker-image and init-letsencrypt.sh script to orchestrate all services
