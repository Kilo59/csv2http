# csv2http

[![ci](https://github.com/Kilo59/csv2http/workflows/ci/badge.svg)](https://github.com/Kilo59/csv2http/actions)
[![pypi version](https://img.shields.io/pypi/v/csv2http.svg)](https://pypi.org/project/csv2http/)
![Python Versions](https://img.shields.io/pypi/pyversions/csv2http)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Kilo59_csv2http&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Kilo59_csv2http)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Kilo59_csv2http&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Kilo59_csv2http)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

CLI tool and library for making a series of JSON or form-encoded HTTP requests based on a CSV file input.

![Demo](images/demo1.svg)

## Quick start

Install

```
pip install csv2http
```

Or with [pipx](https://pypa.github.io/pipx/) (recommended)

```
pipx install csv2http
```

Check CLI usage

```
❯ csv2http --help
usage: csv2http [-h] [-c CONCURRENCY] [--method {POST,PATCH,PUT}] [-a AUTH] [-H [HEADER ...]] [-d] [-n] [-t TIMEOUT] file url

HTTP request for every row of a CSV file - v0.0.3a1

positional arguments:
  file                  payload csv file
  url                   URL destination - called with `http` if scheme is absent

options:
  -h, --help            show this help message and exit
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Maximum number of concurrent requests (default: 25)
  --method {POST,PATCH,PUT}
                        HTTP method/verb (default: POST)
  -a AUTH, --auth AUTH  Basic Authentication enter <USERNAME>:<PASSWORD>. If password is blank you will be prompted for input
  -H [HEADER ...], --header [HEADER ...]
                        Header `key:value` pairs
  -d, --form-data       Send payload as form encoded data instead of JSON (default: false)
  -n, --no-save         Do not save results to log file (default: false)
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout of the request in seconds (default: 5)
```

### Mockbin Example

Make POST calls to http://mockbin.org from a local csv file.

---

First setup a new `bin`, using [httpie](https://httpie.io/cli), curl or the [web ui](http://mockbin.com/bin/create) and get a bin id.

```
❯ http POST mockbin.com/bin/create status:=201 statusText=Created httpVersion=HTTP/1.1 headers:='[]' cookies:='[]' 'content[mimeType]'=application/json --body
"9e95289e-d048-4515-9a61-07f2c74810f5"
```

Create your `my_file.csv` and pass it to `csv2http`.
Use the returned bin id from before.

```
❯ csv2http my_file.csv mockbin.org/bin/9e95289e-d048-4515-9a61-07f2c74810f5 --concurrency 3
 POST http://mockbin.org/bin/mockbin.org/bin/9e95289e-d048-4515-9a61-07f2c74810f5
  status codes - {200: 3}
  status codes - {200: 3}
  status codes - {200: 3}
  status codes - {200: 1}
```

Check the bin log from.
https://mockbin.org/bin/9e95289e-d048-4515-9a61-07f2c74810f5/log

### Set Auth and Headers

Header key, value pairs can be set with the `-H` or `-header` flag.

Key value pairs should be separated with either a `:` or `=`.

```
csv2http my_file.csv httpbin.org/post -H user-agent:csv2http-cli x-custom-header=foobar
```

To provide basic auth pass a username and password with `-a` or `--auth`.

If the password is omitted you will be prompted to provide it.

```
--auth my_username:my_password
```

```
--auth my_username
```

## Roadmap

- [x] As Library - Alpha
  - [x] parse csv as dictionary/json - Alpha
  - [x] accept mutator function - Alpha
  - [x] HTTP POST request with json from csv - Alpha
  - [x] limit concurrency - Alpha
  - [ ] non-blocking file IO - ???
  - [ ] hooks for response results - Beta
  - [ ] mkdoc docs - Beta
- [ ] As CLI - Beta
  - [x] argparse - Alpha
  - [x] write results to logfile - Beta
  - [ ] progress bar - ???
  - [ ] use dedicated CLI library with pretty colors (typer, rich etc.) - Beta
  - [ ] Nested fields - V1
- [ ] Complete Docs - V1
  - [ ] `create_mockbin.csv` and `example.csv` to use in quickstart - Beta
  - [ ] examples for using as library
- [x] GH Actions CI (lint, test, etc.)
- [ ] GH Actions CD (publish to pypi)
