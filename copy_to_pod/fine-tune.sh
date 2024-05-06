#!/bin/bash

tar -xvf /workspace/copy_to_pod/small_data.jsonl.tar.gz -C /workspace/copy_to_pod/

/workspace/copy_to_pod
cd /workspace/axolotl

# PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:128 
# https://gist.github.com/ashmalvayani/b4dee2084ffac9dbddc5dd32353448d3
accelerate launch -m axolotl.cli.train /home/rslm/ABC_scripts/copy_to_pod/config.yml &> ../ft.log