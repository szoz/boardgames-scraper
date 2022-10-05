# Boardgames scraper

Collects data from `https://boardgamegeek.com/` website.

## Top scraper

Collects rank data from top 1000 BGG list.

### Local usage

* Create and activate virtual environment using PipEnv.
* Install dependencies
* Run `main.py`
* Results will be stored in JSON file in the same directory.

### Serverless setup

* Create local environment
* Create new AWS Lambda function.
* Deploy `main.py` file content.
* Create `python` subdirectory and install required packages one by one (boto3 is not required): 
  `pip install --target ./python requests-html==0.10.0`
* Create zip archive with dependencies.
  `zip -r requests_html_layer.zip python`
* Create a new layer on AWS Lambda console and upload archive.
* Create and assign a new execution role on AWS Lambda console with `s3:Put*` action.
* Optionally add a periodic trigger in Event Bridge on AWS console.
* Results will be stored in S3 bucked as JSON files.
