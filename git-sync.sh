d=$(date +"\"[%D]-[%I:%M-%p]\"" )
#git add README.md
git commit -m $d
git push -u origin master