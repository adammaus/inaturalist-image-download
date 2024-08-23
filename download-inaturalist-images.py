##
# Download iNatural images for specific Taxon IDs from Amazon S3 buckets
#
# @WARNING! Use at your own risk. URIs and schema are outside our control and may change at any time. Always double-check @TODOs before using.
#
# References
#		https://registry.opendata.aws/inaturalist-open-data/
#		https://github.com/inaturalist/inaturalist-open-data
#
# Prerequisites
#	* Requires `aws cli` which can be downloaded from: https://aws.amazon.com/cli/
#	* Requires substantial disk space (>200gb)
#		As of Aug 2024, uncompressed datasets are large (Taxa = 175mb, Photos = 31gb, Observations = 15.6gb). This is before images that get downloaded.
#
#	1. Download compressed datasets
#		a. aws s3 cp --no-sign-request s3://inaturalist-open-data/taxa.csv.gz ~/Desktop/taxa.csv.gz
#		b. aws s3 cp --no-sign-request s3://inaturalist-open-data/photos.csv.gz ~/Desktop/photos.csv.gz
#		c. aws s3 cp --no-sign-request s3://inaturalist-open-data/observations.csv.gz ~/Desktop/observations.csv.gz
#	2. Unzip datasets
#
#	3. Determine taxon_id using the taxa.csv and fill out taxon_ids_directory_name_mapping
#
#	4. Adjust @TODOs below
##
import csv, os, subprocess

##
# Path to Photos csv file
# @TODO: Fill in the path on your system
#
# @NOTE: Schema of photos as of Aug 2024 (found on Github)
#	photo_uuid
#	photo_id
#	observation_uuid
#	observer_id
#	extension
#	license
#	width
#	height
#	position
#
# @var string
##
photos_csv_path = os.path.join(os.sep, "Users", "amaus", "Desktop", "photos.csv")

##
# Path to Observations csv file
# @TODO: Fill in the path on your system
#
# @NOTE Schema of observations as of Aug 2024 (found on Github)
#	observation_uuid
#	observer_id
#	x license (in github picture but not actually in data, don't count this)
#	latitude
#	longitude
#	positional_accuracy
#	taxon_id
#	quality_grade
#	observed_on
#
# @var string
##
observations_csv_path = os.path.join(os.sep, "Users", "amaus", "Desktop", "observations.csv")

##
# Directory where to save images
# @TODO: Fill in the path on your system
#
# @NOTE Resulting structure of directory
#	<destination_image_directory>
#		<directory_name for taxon_id_1>
#		<directory_name for taxon_id_2>
#		...
#
# @var string
##
destination_image_directory = os.path.join("original-inaturalist-data")

##
# Mapping betwen taxon_id in taxa.csv to a directory name for the taxon_id such as the species name
# @TODO: Choose your taxon_ids to download and directory names where you store the downloaded images
#
# @var Dictionary (string => string)
##
taxon_ids_directory_name_mapping = {
	"83744": "amblyomma americanum", # lone star tick
	"52155": "dermacentor variabilis", # american dog tick
	"60598": "ixodes scapularis" # black-legged tick
}

##
# Template for S3 Bucket URI
#
# @var string
##
s3_bucket_uri_template = "s3://inaturalist-open-data/photos/[photo_id]/small.[extension]"

##
# Main driver for program
##
def main():
	tick_observation_dict = findTaxonIDObservations()
	print(len(tick_observation_dict), "observations found")
	photo_observation_array = findPhotosByObservations(tick_observation_dict)
	downloadPhotos(photo_observation_array)

##
# Download photos
#
# @param photo_observation_array		Array of photo + observations to download
#
# @return void
##
def downloadPhotos(photo_observation_array):
	for row in photo_observation_array:
		# @TODO: Double check that schema is correct (for photos.csv + observations.csv)
		# Tricky bit: You have to count all of the columns in photos.csv and then observations.csv
		photo_id = row[1]
		extension = row[4]
		taxon_id = row[14]

		# Set a default species if a taxon_id is not found in our mapping. This shouldn't happen...
		species = "unknown"
		if (taxon_id in taxon_ids_directory_name_mapping):
			species = taxon_ids_directory_name_mapping[taxon_id]

		# Determine directory where we store the image, create it if it doesn't already exist
		destination_directory = os.path.join(destination_image_directory, species)
		if (not os.path.exists(destination_directory)):
			os.mkdir(destination_directory)

		destination_image_path = os.path.join(destination_directory, photo_id + "." + extension)

		# Attempt to ignore already downloaded images
		if (os.path.exists(destination_image_path)):
			continue

		# Download image using aws cli
		s3_bucket_url = s3_bucket_uri_template.replace("[photo_id]", photo_id).replace("[extension]", extension)
		subprocess.run(["aws", "s3", "cp", "--no-sign-request", s3_bucket_url, destination_image_path])

##
# Find photos by observations
#
# @param observation_dict 		Structured like observation_uuid => observation
#
# return Array(photo row + observation row)
##
def findPhotosByObservations(observations_dict):
	photos = []
	with open(photos_csv_path, newline='\n') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')

		for row in reader:
			# @TODO: Double check that schema is correct (for photos.csv)
			observation_uuid = str(row[2])

			if (observation_uuid in observations_dict):
				observation_row = observations_dict[observation_uuid].copy()
				photos.append(row + observation_row)
				del observations_dict[observation_uuid] # Helps us jump out of reading the entire dataset if we got everything already

			if (len(observations_dict) == 0):
				break

	return photos


##
# Find Taxon ID by observations
#
# return Dictionary (observation_uuid => observation)
##
def findTaxonIDObservations():
	observations_dict = {}

	with open(observations_csv_path, newline='\n') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')

		for row in reader:
			# @TODO: Double check that schema is correct (for observations.csv)
			observation_uuid = str(row[0])
			taxon_id = str(row[5])

			if (taxon_id in taxon_ids_directory_name_mapping):
				observations_dict[observation_uuid] = row

	return observations_dict

main()