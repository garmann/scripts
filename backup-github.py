#!/usr/bin/env python3

"""
simple python backup script for a github account
it only takes own sources and not forks, stores them as zip file in a folder
forks are skipped at this point, script not supports branch detection or zip creation of all branches
only master branch is saved
"""
try:
    import requests
    import sys
    import datetime
    import os
except ModuleNotFoundError:
    raise Exception('install all modules with: pip install -r requirements.txt')

username = 'garmann'
github_url = 'https://api.github.com/users/' + username + '/repos?per_page=1000'
isodate = datetime.date.isoformat(datetime.date.today())


# connect and process data from github api
# builds up download_data a list with dicts inside
try:
    r = requests.get(github_url)
    
    download_data = []
    for github_repo in r.json():
        if github_repo['fork'] == False:
            data_dict = {}
            data_dict['name'] = github_repo['name']
            data_dict['url'] = 'https://github.com/' + github_repo['full_name'] + '/archive/master.zip'
            download_data.append(data_dict)

except Exception as e:
    raise Exception('cloud not fetch and processs data from github api for: ' + github_url, e)


# create bacukup dir with timestamp
try:
    os.makedirs("backup-" + isodate + "/sources", exist_ok=True)
except Exception as e:
    raise Exception('cloud not create backupdir', e)


# download zip archives from download_data
try:
    for repo in download_data:
        downloaded_file = requests.get(repo['url'], stream=True)
        with open('backup-' + isodate + '/sources/' + repo['name'] + '.zip', 'wb') as f:
            for chunk in downloaded_file.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
except Exception as e:
    raise Exception('could not download and store file', e)


print('done, downloaded files:', len(download_data))
