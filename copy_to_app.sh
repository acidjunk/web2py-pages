#!/bin/bash
# A script to copy the web2py-pages files to an existing app 
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Run this script with an PATH to the application you want to patch. E.g.: ./copy_to_app.sh ../your_awesome_web2py_app "
    exit 1
fi

TARGET_LOCATION=$1
echo "Using $1 as target location"

echo "Are you sure you want to copy the files? You could also use the w2p plugin, this operation could screwup your app. Anwer 'yes' to continue"
read ans
if [ "$ans" != "yes" ]; then
    echo "Quitting"
    exit 1
fi

echo "Merging files in the new tree"
# Controllers
cp -v controllers/page*.py $TARGET_LOCATION/controllers/
cp -v controllers/plugin_tagging.py $TARGET_LOCATION/controllers/
# Modules
cp -v modules/plugin_ckeditor.py $TARGET_LOCATION/modules/
# Models
cp -v models/page*.py $TARGET_LOCATION/models/
cp -v models/0_db.py $TARGET_LOCATION/models/
cp -v models/plugin_ckeditor.py $TARGET_LOCATION/models/
cp -v models/plugin_tagging.py $TARGET_LOCATION/models/
# Views
cp -rv views/page $TARGET_LOCATION/views/
cp -rv views/page_custom $TARGET_LOCATION/views/
cp -rv views/plugin_ckeditor $TARGET_LOCATION/views/
cp -rv views/plugin_tagging $TARGET_LOCATION/views/
#Static assets
cp -rv static/page $TARGET_LOCATION/static/
cp -rv static/plugin_ckeditor $TARGET_LOCATION/static/
cp -rv static/plugin_markitup $TARGET_LOCATION/static/
cp -rv static/plugin_wiki $TARGET_LOCATION/static/
