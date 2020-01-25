# DomDetURL
 Python script to determine desktop and mobile URL of given domain.

## Motivation
[Pi-Hole][PiHole] is a DNS proxy used to filter out advertisements, block some
domains and so on. For my networt at home I'm using a [Pi-Hole][PiHole] and I
am very satisfied with it.

[Pi-Hole][PiHole] enables the user to use many blacklists. So I'm using e. g.
[https://github.com/chadmayfield/my-pihole-blocklists][ChadList] of
[Chad Mayfield][Chad]. I've figured out that some of the domains are blocked,
but not the mobile version of the domain. So I was thinking about a way to
figure out the mobile version of a domain.

## Asumptions
Running this small scripts some assumptions are done:

- The webservers are well configured and redirect the user to the correct URL.
- The request to the domain will always redirect to a valid URL.
- The desktop URL will be determined using a 'desktop browser'.
- The mobile URL will be determined using a 'mobile browser'.
- Based on this assumptions there is no need to figure out all possible subdomains
  and URLs.

## Example

Determine the desktop URL and mobile URL of the domain ```ladies.de```. Using
curl request the domain using a desktop browser:

```
$ curl -I --user-agent "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)" ladies.de
HTTP/1.1 301 Moved Permanently
Content-length: 0
Location: https://ladies.de/
Connection: close
```
The domain is redirected to "https://ladies.de/". So let's check this one:
```
$ curl -I --user-agent "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)" https://ladies.de
HTTP/1.1 301 Moved Permanently
Date: Tue, 31 Dec 2019 16:18:55 GMT
Server: Apache
X-content-age: 18
Location: https://www.ladies.de/
Cache-Control: max-age=0
Expires: Tue, 31 Dec 2019 16:18:55 GMT
Vary: User-Agent
Content-Type: text/html; charset=UTF-8
```
This is again redirected to "https://www.ladies.de/" - let's check this:
```
$ curl -I --user-agent "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)" https://www.ladies.de
HTTP/1.1 200 OK
Date: Tue, 31 Dec 2019 16:20:12 GMT
Server: Apache
X-content-age: 18
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Set-Cookie: PHPSESSID=tieohs55ldcniubg95i5tmdg11; path=/
Set-Cookie: anzeigenmarktPage=1; expires=Wed, 01-Jan-2020 16:20:12 GMT; path=/
Set-Cookie: aktuellesPage=1; expires=Wed, 01-Jan-2020 16:20:12 GMT; path=/
Vary: User-Agent
Content-Type: text/html; charset=UTF-8
```
This seems to be the valid domain. Now let's request this domain with a mobile user-agent:
```
$ curl -I --user-agent "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H)" https://www.ladies.de
HTTP/1.1 307 Temporary Redirect
Date: Tue, 31 Dec 2019 16:21:47 GMT
Server: Apache
X-content-age: 18
Cache-Control: no-cache, max-age=1, must-revalidate, no-store
Pragma: no-cache
Location: https://m.ladies.de/
Cache-Control: max-age=0
Expires: Tue, 31 Dec 2019 16:21:47 GMT
Vary: User-Agent
Content-Type: text/html; charset=UTF-8
```
This is now rediected to "https://m.ladies.de/" - let's check this one, too:
```
$ curl -I --user-agent "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H)" https://m.ladies.de
HTTP/1.1 200 OK
Date: Tue, 31 Dec 2019 16:22:50 GMT
Server: Apache
X-content-age: 18
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Set-Cookie: mobileversion=1; expires=Tue, 14-Jan-2020 16:22:50 GMT; path=/; domain=.ladies.de
Set-Cookie: PHPSESSID=2qbu4h9d1lnhifqk60kuodk8k2; path=/
Vary: User-Agent
Content-Type: text/html; charset=UTF-8
```
Seems to be the default mobile domain.

## Ready to use script

Spending a saturday afternoon I've made a simple Python script to do this
automagically. The prerequisites are:

- Installed Python package [```logging```][PyLogging]
- Installed Python package [```requests```][PyRequests]

## How to use
The script is very simple to use. On your commandline just call e. g.

```Python
python program.py ladies.de heise.de dumbdomain
```

The results of the script will be logged to the file ```program.log```:

```Python
2020-01-25 16:42:11,244 | INFO | <module> | startup
2020-01-25 16:42:14,950 | INFO | <module> | domains [{'DOMAIN': 'ladies.de', 'DESKTOP': 'https://www.ladies.de/', 'MOBILE': 'https://m.ladies.de/'}]
2020-01-25 16:42:15,128 | INFO | <module> | domains [{'DOMAIN': 'heise.de', 'DESKTOP': 'https://www.heise.de/', 'MOBILE': 'https://www.heise.de/'}]
2020-01-25 16:42:17,387 | INFO | geturl | Connection error for [http://dumbdomain]: [HTTPConnectionPool(host='dumbdomain', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001F09EA02820>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))]
2020-01-25 16:42:19,642 | INFO | geturl | Connection error for [http://dumbdomain]: [HTTPConnectionPool(host='dumbdomain', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001F09EA02040>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))]
2020-01-25 16:42:19,642 | INFO | <module> | domains [{'DOMAIN': 'dumbdomain', 'DESKTOP': 'http://dumbdomain', 'MOBILE': 'http://dumbdomain'}]
```

[ChadList]: https://github.com/chadmayfield/my-pihole-blocklists
[Chad]: https://github.com/chadmayfield
[PiHole]: https://pi-hole.net/
[PyLogging]: https://pypi.org/project/logging/
[PyRequests]: https://pypi.org/project/requests/