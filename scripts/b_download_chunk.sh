#!/bin/bash
# TODO: Clean up paths
# chunk number from 00 to 99
CHUNK_NUM=$1

echo "CHUNK_NUM: $CHUNK_NUM"

# 0. Install dependencies
apt-get update && apt-get install -y wget p7zip-full p7zip-rar

#
# 1. Download 7z of meta files
#
echo 'Downloading meta files...'

if [[ -f meta_v00.txt ]]; then
  rm meta_v00.txt
fi
wget https://deep-geometry.github.io/abc-dataset/data/meta_v00.txt
if [[ -d ./dataset/meta_compressed_$CHUNK_NUM ]]; then
  rm -rf ./dataset/meta_compressed_$CHUNK_NUM
fi
mkdir -p ./dataset/meta_compressed_$CHUNK_NUM
sed -n "$((CHUNK_NUM+1))p" meta_v00.txt | \
    xargs -n 2 -P 32 sh -c \
        "wget --no-check-certificate \$0 -O ./dataset/meta_compressed_$CHUNK_NUM/\$1"

#
# 2. Extract 7z of meta files
#
echo 'Extracting meta files...'

if [[ -d ./dataset/meta_extracted_$CHUNK_NUM ]]; then
    rm -rf ./dataset/meta_extracted_$CHUNK_NUM
fi
mkdir ./dataset/meta_extracted_$CHUNK_NUM

# extract .7z files from ./dataset/meta
find ./dataset/meta_compressed_$CHUNK_NUM -name '*.7z' | \
    xargs -n 1 -P 32 sh -c "7z e \$0 -o./dataset/meta_extracted_$CHUNK_NUM"

# delete directories that it also extracts
find ./dataset/meta_extracted_$CHUNK_NUM -type d -delete

#
# 4. Download .7z's of .step files
#
echo 'Downloading step files...'

if [[ -f step_v00.txt ]]; then
  rm step_v00.txt
fi
wget https://deep-geometry.github.io/abc-dataset/data/step_v00.txt
if [[ -d ./dataset/step_compressed_$CHUNK_NUM ]]; then
    rm -rf ./dataset/step_compressed_$CHUNK_NUM
fi
mkdir -p ./dataset/step_compressed_$CHUNK_NUM
sed -n "$((CHUNK_NUM+1))p" step_v00.txt | \
    xargs -n 2 -P 32 sh -c \
        "wget --no-check-certificate \$0 -O ./dataset/step_compressed_$CHUNK_NUM/\$1"

#
# 5. Extract .step files
#
echo 'Extracting step files...'

if [[ -d ./dataset/step_extracted_$CHUNK_NUM ]]; then
    rm -rf ./dataset/step_extracted_$CHUNK_NUM
fi
mkdir ./dataset/step_extracted_$CHUNK_NUM

# extract .7z files from ./dataset/step
find ./dataset/step_compressed_$CHUNK_NUM -name '*.7z' | \
    xargs -n 1 -P 32 sh -c "7z e \$0 -o./dataset/step_extracted_$CHUNK_NUM"

# delete directories that it also extracts
find ./dataset/step_extracted_$CHUNK_NUM -type d -delete

#
# 6. Clean up
#
rm -rf ./dataset/step_compressed_$CHUNK_NUM
rm -rf ./dataset/meta_compressed_$CHUNK_NUM

echo 'Download successful.'
