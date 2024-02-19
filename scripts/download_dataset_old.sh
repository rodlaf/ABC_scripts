#!/bin/bash

# chunk number from 00 to 99
CHUNK_NUM=00

#
# 1. Download 7z's of meta files
#
# wget https://deep-geometry.github.io/abc-dataset/data/meta_v00.txt
# if [[ -d ./dataset/meta ]]; then
#   rm -rf ./dataset/meta
# fi
# mkdir ./dataset/meta
# cat meta_v00.txt | xargs -n 2 -P 32 sh -c -c 'wget --no-check-certificate $0 -O ./dataset/meta/$1'

#
# 2. Extract 7z's of meta files
#
# if [[ -d ./dataset/meta_extracted ]]; then
#     rm -rf ./dataset/meta_extracted
# fi
# mkdir ./dataset/meta_extracted

# # extract .7z files from ./dataset/meta
# find ./dataset/meta -name '*.7z' | xargs -n 1 -P 32 sh -c '7z e $0 -o./dataset/meta_extracted'

# # delete directories that it also extracts
# find ./dataset/meta_extracted -type d -delete

# echo 'Extraction successful.'

#
# 3. Isolate files with usable names (maybe?)
#
# if [[ -f ./dataset/usable_files.txt ]]; then
#     rm ./dataset/usable_files.txt
# fi
# touch ./dataset/usable_files.txt

# ls ./dataset/meta_extracted | xargs -n 1 -P 32 sh -c ''

#
# 4. Download .7z's of .step files
#
# wget https://deep-geometry.github.io/abc-dataset/data/step_v00.txt
# if [[ -d ./dataset/step ]]; then
#     rm -rf ./dataset/step
# fi
# mkdir ./dataset/step
# cat step_v00.txt | xargs -n 2 -P 32 sh -c 'wget --no-check-certificate $0 -O ./dataset/step/$1'

#
# 5. Extract .step files
#
if [[ -d ./dataset/step_extracted ]]; then
    rm -rf ./dataset/step_extracted
fi
mkdir ./dataset/step_extracted

# extract .7z files from ./dataset/step
find ./dataset/step -name '*.7z' | xargs -n 1 -P 32 sh -c '7z e $0 -o./dataset/step_extracted'

# delete directories that it also extracts
find ./dataset/step_extracted -type d -delete

# echo 'Extraction successful.'

#
# 6. Generate dataset from usable .step files and their descriptions
#