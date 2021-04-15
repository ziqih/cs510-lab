# CommonCrawl Crawler

The crawler works in 2 phases. We first retrieve the meta info that matches up with the provided domains. Then a script will download all the urls retrieved in the first phase.

### Prepare

Prepare a list of domains of interest and put them into a file, where each line is one domain. We provide the "all_domains.csv" used in our process.

Create a folder `crawl` in the current folder. Later the script will generate 3 subfolders:

* **crawl/list** meta info retrieved from common crawl for the provided domains
* **crawl/warc** downloaded raw pages
* **crawl/rec** detailed info connecting the downloaded image and the original url

### Usage

1. Start the index client to retrieve all the urls matching the domains provided in the domain file. The result list files will be generated in `crawl/list`.

```bash
python cdx-index-client.py -c CC-MAIN-2021-04 ""  -d crawl/list --json --target-domain-file all_domains.csv
```

2. Start the download script, this reads the `crawl/list` folder and download all the pages recorded. Now all the pages are in `crawl/warc`.

```bash
bash run_download.sh
```

3. (option) If a detailed record of all the successfully downloaded urls is desired, run the merge script that checks through rec and warc and generates a single record file.

```bash
python merge_warc.py crawl/ crawl/crawled.pkl
```

All "*.pkl" file is in pandas pickle.