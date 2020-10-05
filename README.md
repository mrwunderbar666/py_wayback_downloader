# py_wayback_downloader
Python Implementation of a web.archive.org downloader. Download snapshots of entire websites from the archive. Perfect for internet archaeology, scraping, or making backups.

**Requires Python3.7 or higher**

# Features and usage

This python script is inspired by a [tool written in Ruby](https://github.com/hartator/wayback-machine-downloader) and mimics a lot of its functionality. It downloads entire webpages that were archived on [web.archive.org](http://web.archive.org/) within a specified time frame. All pages are stored locally in the original file format (e.g. html, jpg, etc).

Files are stored in a output folder that is created on the first run. The pathing is structured as `output/{domain}/{timestamp}/{files}`. So a download from January 31, 2005 of www.example.com will be stored in `output/example.com/20050131/file.html`.

Existing files are not overwritten and skipped! So if you have to cancel a download, you can easily resume it any time.

## Getting started

Download this repository with:

```
git clone https://github.com/mrwunderbar666/py_wayback_downloader.git
```

Make sure you have `tqdm` installed:

```
pip install tqdm
```

Then, you can start right away and download your desired webpage. The default setting downloads *all* pages from *all* snapshots from the past 365 days:
```
python wbmdownloader.py http://example.com
```


Let's say you want to download www.example.com from March and April 2007. You just have to write the date in a timestamp format like YYYYMMDD. March 2007 is `200703`, and 21 January 2012 is `20120121`:

```
python wbmdownloader.py http://example.com --from 200703 --to 200704
```

If you want to speed it up, you can use concurrent downloads via the `--threads` argument. Let's say we want 8 downloads simultaneously:
```
python wbmdownloader.py http://example.com --from 200703 --to 200704 --threads 8
```

## Additional arguments

### Only list files

If you don't want to download the actual files, and just get a list of files, add the `--list` flag. This is useful, if you want to dry run a large download.

### Only get exact url

By default, the script will get all files that are nested under the base url. If you add the `--exact-url` flag, only the specified url will be downloaded (without any children).

### Download all file types

By default, the script only downloads files that are marked as `text/html`. If you want to download all file types, then you add the `--all-types` flag.

### Download all status codes

By default, the script skips over pages that do not give response code 200. If you want to include 3xx, 4xx add the `--all-codes` flag.


### Add custom filter

The webarchive cdx server API allows for regex filtering. Maybe you want to check [their reference guide](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) for that.

You can filter by specific meta information fields: `urlkey`, `timestamp`, `original`, `mimetype`,`statuscode`, `digest`, `length` (file length).

The most useful ones are `original` (original url path) and `mimetype` (file type). Let's say you want to keep only urls that have the string `article` in it:

```
python wbmdownloader.py http://example.com --filter original:.*article.* --from 200703 --to 200704 --threads 8
```


# Contribute & Issues

Just raise an issue or drop me a friendly message. Contributions are welcome!