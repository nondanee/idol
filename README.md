<img src="https://user-images.githubusercontent.com/26399680/57981044-44703280-7a65-11e9-986c-b04c28d220bd.png" width="144" height="144" align="right" />

# idol ![](https://img.shields.io/badge/python-3.4+-blue.svg?style=flat-square)

Blog content aggregator webapp for Sakamichi46 ◢

*Powered by Aiohttp & MySQL*

## Main work

- Blog reformat and high-res photo predownload (for awalker dcimg)
- Optimized machine translating does some help for reading
- Archive all keyakizaka members' blog and a part of nogizaka graduation's blog
- Separate blog from group channel for each of new-joined members
- ~~New blog posting reminder subscription (FCM push involved in PWA feature)~~

## Service status

- Text data and API service are hosted on Vultr VC2
- Photos are stored in Google cloud storage

> Finding sponsors and maintainers

## Quick start

1. Fill your personal account setting (including Translation API, OSS access, RDS connection) in two file with `.example` suffix and rename them to `.py` file before starting server and crawler
2. Install dependency for server and crawler by the corresponding `requirements.txt`
3. Create new database and execute table creating SQL and fill member information by the file in `init/` directory
4. You can run `python crawler/manage.py -h` for arguments about crawling and run `python server/main.py` to start API server
5. You will need Nginx to host static files in `host/` directory, and a process management tool to keep server always run. In the `config/` directory, there are nginx and supervisor configuration examples for reference

## Public API

### Feed

**GET** `/api/feed/all` 

Mixed blog from nogizaka/keyakizaka/hinatazaka members in post time descending order

- `size` 1 ~ 100 (default is 10)
- `page` start from 1

**GET** `/api/feed/member/:id:` 

Blog from a specific member in post time descending order (Please refer member.txt for member id)

- `size` *ditto*
- `page` *ditto*

**GET** `/api/free` 

Blog from a specific group in post time descending order (Structure of response data is different from the first one)

- `group` nogizaka|keyakizaka

- `size` *ditto*
- `page` *ditto*

### Blog

id is a 7 digits number, please pad the number space with zero first

For nogizaka, remain the first digit with 0; for keyakizaka and hinatazaka, set the first digit to 1

**GET** `/api/diary/:id:`

Markdown-liked blog data in JSON format

**GET** `/api/blog/:id:`

Webpage for blog viewing rendered by JS

## License

MIT