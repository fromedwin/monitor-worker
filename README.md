# monitor-client

Monitor from edwin: Prometheus + Blackbox

## Clone monitor-client repository

```
$> git clone https://github.com/fromedwin/monitor-client.git
```

## Run

```
$> ./run.sh
```

## Configure

Define basic authentication credentials for NGINX using apache2-utils. Verify that apache2-utils (Debian, Ubuntu) or httpd-tools (RHEL/CentOS/Oracle Linux) is installed. (See [documentation](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/) for details)

```
$> sudo htpasswd -cm .htpasswd user1
$> sudo htpasswd .htpasswd user2
```

You can confirm that the file contains paired usernames and encrypted passwords:

```
$ cat .htpasswd
user1:$apr1$/woC1jnP$KAh0SsVn5qeSMjTtn0E9Q0
user2:$apr1$QdR8fNLT$vbCEEzDj7LyqCMyNpSoBh/
user3:$apr1$Mr5A0e.U$0j39Hp5FfxRkneklXaMrr/
```
## Resources

- [Awesome Prometheus Rules](https://awesome-prometheus-alerts.grep.to/rules.html)
