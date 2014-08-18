#!/usr/bin/python

import requests, re, os, shutil, json, sys

if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = raw_input('Enter a target ID or username (e.g. me OR nike): ')

# i have my access token in a file named access_token
# but you could also just assign it to this variable
try:
    my_token = open("access_token", "r").read().strip()
except IOError:
    print "\naccess_token file does not exist.  Get it \n" \
    "from https://developers.facebook.com/tools/explorer, \n" \
    "make sure you grant access to user_photos and save the \n" \
    "contents to a file named access_token in this directory.\n"
    exit()

albums_path = os.path.join(os.getcwd(), target + '_albums')
data_path = albums_path + '/data'

# creating data and album directories if they don't exist
if not os.path.exists(data_path):
    os.makedirs(data_path)

if not os.path.exists(albums_path):
    os.makedirs(albums_path)

json_filename = os.path.join(data_path, "album_list.json")

if not os.path.exists(json_filename):
    # getting all album details for the token's user
    r = requests.get("https://graph.facebook.com/%s/albums?fields=name&limit=100&access_token=%s" % (target, my_token))

    # dropping out if we get a bad http response
    if r.status_code != 200:
        print "\nFailed to properly connect to the Facebook API."
        print "HTTP Status Code: %s\n" % r.status_code
        exit()

    # saving JSON response for the album list
    json_file = open(json_filename, "w")
    json_file.write(json.dumps(r.json(), sort_keys=True,
                               indent=4, separators=(',', ': ')))
    json_file.close()

    # a dict representation of albums data
    albums = r.json()['data']
else:
    json_file = open(json_filename, "r")
    albums = json.load(json_file)["data"]
    json_file.close()


# for stripping non-alphanumeric
pattern = re.compile('[\W]+')

for album in albums:
    print 'Processing album "%s" with id %s.' % (album['name'], album['id'])

    album_dir_name = pattern.sub('', album['name'].replace(' ','_'))
    album_path = os.path.join(albums_path, album_dir_name)

    if not os.path.exists(album_path):
        os.makedirs(album_path)

    json_filename = os.path.join(data_path, "%s.json" % album_dir_name)

    if not os.path.exists(json_filename):
        r2 = requests.get("https://graph.facebook.com/%s/photos?fields=source&limit=1000&access_token=%s"
                          % (album['id'], my_token))
        # saving JSON response for the image list
        json_file = open(json_filename, "w")
        json_file.write(json.dumps(r2.json(), sort_keys=True,
                                   indent=4, separators=(',', ': ')))
        json_file.close()

        images = r2.json()["data"]
    else:
        json_file = open(json_filename, "r")
        images = json.load(json_file)["data"]
        json_file.close()

    for counter, image in enumerate(images):
        counter += 1
	createtime = image["created_time"].replace(":","-")
        timeid = "%s %s" % (createtime, image["id"])
        image_filename = os.path.join(album_path, "%s.jpg" % timeid)

        if not os.path.exists(image_filename):
            print "Downloading image %s of album %s." % (counter, album['name'])
            r3 = requests.get(image["source"], stream=True)
            image_file = open(image_filename, "wb")
            shutil.copyfileobj(r3.raw, image_file)
            image_file.close()
        else:
            print "Already retreived image %s of album %s." % (counter, album['name'])

#        if image.has_key('name'):
            #print image["name"]
