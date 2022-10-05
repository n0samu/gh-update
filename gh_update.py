import sys
import os
import shutil
import configparser
import re
import requests

def read_bool(s: str) -> bool:
	try:
		return s.lower() == 'true'
	except:
		return False

def not_prerelease(release: dict) -> bool:
	return not(release.get('prerelease'))

# Uses global variable: asset_regex
def match_asset(asset: dict) -> re.Match:
	return re.match(asset_regex, asset['name'])

def check_for_update(repo: str, last_update: str, include_prerelease: bool) -> dict:
	api_url = f'https://api.github.com/repos/{repo}/releases'
	releases = requests.get(api_url).json()
	if releases:
		if include_prerelease:
			release = releases[0]
		else:
			release = next(filter(not_prerelease, releases), None)
		if release and last_update < release['published_at']:
			return release

def download_asset(asset: dict) -> str:
	req = requests.get(asset['browser_download_url'])
	filename = asset['name']
	with open(filename, 'wb') as fd:
		for chunk in req.iter_content(chunk_size=128):
			fd.write(chunk)
	return filename

if len(sys.argv) != 3:
	sys.exit(f'Usage: python {sys.argv[0]} config.ini asset_name')
config_file = sys.argv[1]
asset_name = sys.argv[2]
if not os.path.isfile(config_file):
	sys.exit('The specified config file was not found')

config = configparser.ConfigParser()
config.read(config_file)
try: 
	main_cfg = config['general']
	repo_name = main_cfg['repo']
	include_prerelease = read_bool(main_cfg['download_prerelease'])
except:
	sys.exit('Wrong config file format')
try:
	asset_cfg = config[asset_name]
	update_path = asset_cfg['extract_path']
	asset_regex = re.compile(asset_cfg['regex'])
except:
	sys.exit('Invalid asset name or regex')

last_update = asset_cfg.get('installed_date', '')
new_release = check_for_update(repo_name, last_update, include_prerelease)
if not new_release:
	sys.exit('No update found')

asset = next(filter(match_asset, new_release['assets']), None)
if not asset:
	sys.exit('No update found')

release_name = new_release['name']
release_time = new_release['published_at']
backup_path = asset_cfg.get('backup_path')
installed_release = asset_cfg.get('installed_name')
delete_files = read_bool(asset_cfg.get('delete_files'))
try:
	asset_file = download_asset(asset)
	if installed_release:
		if backup_path:
			shutil.copytree(update_path, os.path.join(backup_path, installed_release))
		if delete_files:
			shutil.rmtree(update_path)
	shutil.unpack_archive(asset_file, update_path)
	os.remove(asset_file)
	asset_cfg['installed_name'] = release_name
	asset_cfg['installed_date'] = release_time
	config[asset_name] = asset_cfg
	with open(config_file, 'w') as cf:
		config.write(cf)
	print('Update finished!')
except:
	print('Update failed')
