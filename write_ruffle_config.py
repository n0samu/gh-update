import configparser

assets = {
	'linux': '.*linux-x86_64\\.tar\\.gz',
	'macos': '.*macos-universal\\.tar\\.gz',
	'win32': '.*windows-x86_32\\.zip',
	'win64': '.*windows-x86_64\\.zip',
	'selfhosted': '.*web-selfhosted\\.zip',
	'chrome': '.*web-extension\\.zip',
	'firefox': '.*web-extension-firefox.*\\.xpi'
}

config = configparser.ConfigParser()
config['general'] = {
	'repo': 'ruffle-rs/ruffle',
	'download_prerelease': 'True'
}
for name, regex in assets.items():
	config[name] = {
		'regex': regex,
		'extract_path': f'ruffle-{name}',
		'backup_path': ''
	}

with open('ruffle.ini', 'w') as configfile:
	config.write(configfile)
