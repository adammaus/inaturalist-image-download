# Download iNatural images for specific Taxon IDs from Amazon S3 buckets

**@WARNING! Use at your own risk. URIs and schema are outside our control and may change at any time. Always double-check @TODOs before using.**

## References
* https://registry.opendata.aws/inaturalist-open-data/
* https://github.com/inaturalist/inaturalist-open-data

## Prerequisites
* Requires `aws cli` which can be downloaded from: https://aws.amazon.com/cli/
* Requires substantial disk space (>200gb)
  * As of Aug 2024, uncompressed datasets are large (Taxa = 175mb, Photos = 31gb, Observations = 15.6gb). This is before images that get downloaded.

## Running the script
1. Download compressed datasets
	1. aws s3 cp --no-sign-request s3://inaturalist-open-data/taxa.csv.gz ~/Desktop/taxa.csv.gz
	2. aws s3 cp --no-sign-request s3://inaturalist-open-data/photos.csv.gz ~/Desktop/photos.csv.gz
	3. aws s3 cp --no-sign-request s3://inaturalist-open-data/observations.csv.gz ~/Desktop/observations.csv.gz

2. Unzip datasets

3. Determine taxon_id using the taxa.csv and fill out taxon_ids_directory_name_mapping

4. Adjust @TODOs below
