#!/bin/bash

SCRIPTS_DIR=/root/ABC_scripts/scripts
DATASET_DIR=/root/ABC_scripts/dataset

for chunk_num in $(seq 0 99);
do
    echo "chunk_num: $chunk_num"

    META_EXTRACTED_DIR=$DATASET_DIR/meta_extracted_$chunk_num
    STEP_EXTRACTED_DIR=$DATASET_DIR/step_extracted_$chunk_num

    # download
    bash $SCRIPTS_DIR/download_chunk.sh $chunk_num

    # format
    python $SCRIPTS_DIR/format_chunk.py --chunk_num $chunk_num

    # delete download
    rm -rf $META_EXTRACTED_DIR
    rm -rf $STEP_EXTRACTED_DIR
done
