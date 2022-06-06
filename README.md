# csv2http

[![ci](https://github.com/Kilo59/csv2http/workflows/ci/badge.svg)](https://github.com/Kilo59/csv2http/actions)

## Quick start

Install

```
pip install csv2http
```

Check CLI usage

```
❯ csv2http --help
usage: csv2http [-h] [-c CONCURRENCY] [--method {POST,PATCH,PUT}] file url

HTTP request for every row of a CSV file

positional arguments:
  file                  payload csv file
  url                   URL destination - called with `http` if scheme is absent

options:
  -h, --help            show this help message and exit
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Maximum number of concurrent requests (default: 25)
  --method {POST,PATCH,PUT}
                        HTTP method/verb (default: POST)
```

### Mockbin Example

Make POST calls to http://mockbin.org from a local csv file.

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
  - [ ] progress bar - ???
  - [ ] use dedicated CLI library (typer, rich etc.) - Beta
  - [ ] Nested fields - V1
- [ ] Complete Docs - V1
  - [ ] `create_mockbin.csv` and `example.csv` to use in quickstart - Beta
- [x] GH Actions CI (lint, test, etc.)
- [ ] GH Actions CD (publish to pypi)
