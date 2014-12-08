**get_albums.py**

*A utility to quickly pull down a user or pages' Facebook albums.*

This utility creates two directories:
* [target]_albums - folder where album content is stored (prefixed by the target ID/username) 
* [target]_albums/data - folder where Graph API JSON data is cached/stored
 

**PREREQUISITES**

This requires the python requests library.

    pip install requests

The other Python modules in use are built-ins.  This has been tested under Windows 8.1 with Python 2.7.4

It also requires an access token which can be retrieved from the [Graph API Explorer](https://developers.facebook.com/tools/explorer) and placed in the same directory as this script in a file named "access_token".

If you have an access token, application ID application secret key, a longer lasting access token can be retrieved from:
`https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=[app_id]&client_secret=[app_secret]&fb_exchange_token=[short_lived_token]`

**USAGE**

    cd get_albums.py
    echo [access_token_from_api_explorer] > access_token
    get_albums.py

**NOTES**

Uploads to the "Mobile Uploads" album are merged with "Timeline Photos" album.  File names are stored as date (ISO 8601 with `:` replaced with `-`) _ objectID.
