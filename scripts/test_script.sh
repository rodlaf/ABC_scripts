#!/bin/bash

CHUNK_NUM=$1
echo "CHUNK_NUM: $CHUNK_NUM"
echo "$((CHUNK_NUM+1))p"
# echo ${sed -n "$((CHUNK_NUM+1))p" meta_v00.txt}