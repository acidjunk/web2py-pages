#!/bin/bash
#Copy complete stuff to app
echo "Do you really want to run this? it will delete the previous copy..."
echo "It needs a reference web2py app to operate"

EMPTY_REFERENCE_PATH=~/GIT/web2py/applications/welcome
TARGET_LOCATION=~/GIT/web2py/applications/page1_ref

echo "Anwer 'yes' to continue"
read ans
if [ "$ans" != "yes" ]; then
    echo "Quitting"
    exit
fi

echo "Starting delete"
rm -rf $TARGET_LOCATION
echo "Copying reference app"
cp -rv $EMPTY_REFERENCE_PATH $TARGET_LOCATION


echo "Merging module in the new tree"
cp -rv controllers $TARGET_LOCATION/
cp -rv modules $TARGET_LOCATION/
cp -rv models $TARGET_LOCATION/
cp -rv views $TARGET_LOCATION/
cp -rv static $TARGET_LOCATION/
