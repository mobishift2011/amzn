array=( beyondtherack bluefly gilt hautelook ideeli modnique myhabit nomorerack onekingslane ruelala venteprivee zulily lot18 totsy )
for i in "${array[@]}"
do
    mongo $i --eval "db.dropDatabase();"
done
mongo monitor --eval "db.task.remove();"
ssh root@integrate.favbuy.org "mongo mastiff --eval 'db.product.drop();db.event.drop()'"
ssh root@integrate.favbuy.org "curl -XDELETE http://localhost:9200/mastiff"
