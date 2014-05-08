tar -cvzf ../web2py-pages-with-languages.w2p views/ controllers/ modules/ models/ static/ languages/
tar -cvzf ../web2py-pages-without-languages.w2p views/ controllers/ modules/ models/ static/ 
echo "Shall I copy the w2p file to release location? y/n "
read ans
if [ ${ans} == 'y' ]; then
    cp ../web2py-pages*.w2p ~/Dropbox/Public
fi
