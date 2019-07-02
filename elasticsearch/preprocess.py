import os
import time
from tqdm import tqdm
from smappdragon import JsonCollection

def unzip_json(dir, year):
	file_list = os.listdir(os.path.join('/archive/x/xz2448/new_tweets', year, dir))
	zips = [f for f in file_list if f.endswith('.zip')]
	counter = 0
	for zipped in zips:
		unzipped_name = os.path.join('/scratch/xz2448/new_tweets', year, dir, zipped).replace('.zip', '')
		cmd = 'unzip ' + os.path.join('/archive/x/xz2448/new_tweets', year, dir, zipped) + ' -d ' + os.path.join('/scratch/xz2448/new_tweets', year, dir)
		os.system(cmd)
		counter += 1
		if counter%100 == 0:
			print('Unzipped {} files'.format(counter))

def mkdir(path):
	os.makedirs(path, exist_ok=True)

### functions that strip json files, write data in es format, and fuzzy search:
def strip_data(database_dir, stripped_dir):
	"""
	-Args:
		@database_dir: absolute path of the database containing all unzipped json (either '<...>/2014' or '<...>/2015')
		@stripped_dir: absolute path of stripped json files
	-Return:
		None, but saves stripped json files with the same hierarchial structure as that of orginal database
	"""
	mkdir(stripped_dir)
	d_list = list(filter(lambda x: x[:5] == 'state', list(os.listdir(database_dir))))
	try:
		d_list.remove('.DS_Store')
	except:
		pass
	for d in d_list:
		count = 0
		failed = 0
		mkdir(os.path.join(stripped_dir, d))
		dir_path = os.path.join(database_dir, d, 'unzip') # Special case for the current example database
		f_list = filter(lambda x: x[-4:] == 'json', os.listdir(dir_path))
		for f in tqdm(f_list):
			count += 1
			try:
				collection_temp = JsonCollection(os.path.join(dir_path, f))
				stripped = collection_temp.strip_tweets(['id', 'text', 'created_at', 'user.location'])
				output_json = os.path.join(stripped_dir, d, f)
				stripped.dump_to_json(output_json)
			except:
				failed += 1
				pass
		print('Among {} json files in directory {}, {} were successfully stripped using smappdragon.'.format(count, d, count - failed))


def main():
	yr_list = ['2014', '2015']

	## Unzipping the json.zip files
	for year in yr_list:
		start = time.time()
		Tweets_dir = os.path.join('/archive/x/xz2448/new_tweets', year)
		for directory in os.listdir(Tweets_dir):
			print('Start unzipping {}...'.format(directory))
			unzip_json(directory, year)
			print('Finished unzipping {}.'.format(directory))
		end = time.time()
		print('Unzipped all tweets ({}) in {} seconds.'.format(year, end-start))

	## Stripping the unzipped json files (only keeps the id, text, and part of user information)
	for year in yr_list:
	database_dir = os.path.join('/scratch/xz2448/new_tweets', year)
	stripped_dir = os.path.join('/scratch/xz2448/es_twitter', year)
	print('Start stripping all raw json files in {} directory...'.format(year))
	start = time.time()
	strip_data(database_dir, stripped_dir, omit_dir)
	end = time.time()
	print('Finished stripping all raw json files in {} directory. Used {} seconds.'.format(year, end-start))



if __name__ == "__main__":
	main()