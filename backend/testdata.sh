#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: ./testdata.sh <port>, where port is usually either 5000 (local) or 8000 (Docker)"
    exit 1
fi

doRequest() {
    curl --request $1 \
        --url "http://localhost:$2/$3" \
        --header 'content-type: application/json' \
        --data "$4"
}

putReq() {
    doRequest "PUT" "$1" "$2" "$3"
}

postReq() {
    doRequest "POST" "$1" "$2" "$3"
}

putReq $1 'manage/bars/test' '{
    "name": "Test Bar",
    "description": "A test bar",
    "image": "Foobar.jpg"
}'

putReq $1 'manage/bars/digibar' '{
    "name": "The Digi Bar",
    "description": "Your online bar!",
    "image": "Foobay.jpg"
}'

putReq $1 'manage/bars/test/tables/one' ''
putReq $1 'manage/bars/test/tables/other' ''
putReq $1 'manage/bars/digibar/tables/1' ''
putReq $1 'manage/bars/digibar/tables/2' ''

putReq $1 'manage/bars/test/drinks/simple-beer' '{
    "name": "A simple Beer",
    "price": 2
}'
putReq $1 'manage/bars/test/drinks/not-so-simple-beer' '{
    "name": "A not so simple Beer",
    "price": 20
}'
putReq $1 'manage/bars/digibar/drinks/beer' '{
    "name": "Just Beer",
    "price": 2
}'

postReq $1 'manage/bars/digibar/music' '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "playbackPosition": "0:00"
}'