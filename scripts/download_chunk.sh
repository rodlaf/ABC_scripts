#!/bin/bash

# chunk number from 00 to 99
CHUNK_NUM=$1
echo "CHUNK_NUM: $CHUNK_NUM"

DATASET_DIR=/root/ABC_scripts/dataset
META_COMPRESSED_DIR=$DATASET_DIR/meta_compressed_$CHUNK_NUM
META_EXTRACTED_DIR=$DATASET_DIR/meta_extracted_$CHUNK_NUM
STEP_COMPRESSED_DIR=$DATASET_DIR/step_compressed_$CHUNK_NUM
STEP_EXTRACTED_DIR=$DATASET_DIR/step_extracted_$CHUNK_NUM

#
# 0. Install dependencies
#
apt-get update && apt-get install -y wget p7zip-full p7zip-rar

#
# 1. Download 7z of meta files
#
echo 'Downloading meta files...'

if [[ -f meta_v00.txt ]]; then
  rm meta_v00.txt
fi
wget https://deep-geometry.github.io/abc-dataset/data/meta_v00.txt
if [[ -d $META_COMPRESSED_DIR ]]; then
  rm -rf $META_COMPRESSED_DIR
fi
mkdir -p $META_COMPRESSED_DIR
sed -n "$((CHUNK_NUM+1))p" meta_v00.txt | \
    xargs -n 2 -P 32 sh -c \
        "wget --no-check-certificate \$0 -O $META_COMPRESSED_DIR/\$1"

#
# 2. Extract 7z of meta files
#
echo 'Extracting meta files...'

if [[ -d $META_EXTRACTED_DIR ]]; then
    rm -rf $META_EXTRACTED_DIR
fi
mkdir $META_EXTRACTED_DIR

# extract .7z files from ./dataset/meta
find $META_COMPRESSED_DIR -name '*.7z' | \
    xargs -n 1 -P 32 sh -c "7z e \$0 -o$META_EXTRACTED_DIR"

# delete directories that it also extracts
find $META_EXTRACTED_DIR -type d -delete

#
# 4. Download .7z's of .step files
#
echo 'Downloading step files...'

if [[ -f step_v00.txt ]]; then
  rm step_v00.txt
fi
wget https://deep-geometry.github.io/abc-dataset/data/step_v00.txt
if [[ -d $STEP_COMPRESSED_DIR ]]; then
    rm -rf $STEP_COMPRESSED_DIR
fi
mkdir -p $STEP_COMPRESSED_DIR
sed -n "$((CHUNK_NUM+1))p" step_v00.txt | \
    xargs -n 2 -P 32 sh -c \
        "wget --no-check-certificate \$0 -O $STEP_COMPRESSED_DIR/\$1"

#
# 5. Extract .step files
#
echo 'Extracting step files...'

if [[ -d $STEP_EXTRACTED_DIR ]]; then
    rm -rf $STEP_EXTRACTED_DIR
fi
mkdir $STEP_EXTRACTED_DIR

# extract .7z files from ./dataset/step
find $STEP_COMPRESSED_DIR -name '*.7z' | \
    xargs -n 1 -P 32 sh -c "7z e \$0 -o$STEP_EXTRACTED_DIR"

# delete directories that it also extracts
find $STEP_EXTRACTED_DIR -type d -delete

#
# 6. Clean up
#
rm meta_v00.txt
rm step_v00.txt
rm -rf $STEP_COMPRESSED_DIR
rm -rf $META_COMPRESSED_DIR
