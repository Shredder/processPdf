#!/usr/bin/env zsh

keyWords=(${@[0,-2]})
keyWords=(-keywords=${^keyWords})

file="${@[-1]}"

if [[ ${#keyWords} == 0 ]]; then
    cmd="exiftool -keywords $file"
else
    cmd="exiftool $keyWords $file"
fi
eval $cmd
