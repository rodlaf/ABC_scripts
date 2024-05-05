#!/bin/bash

tar -xvf /workspace/copy_to_pod/small_data.jsonl.tar.gz -C /workspace/copy_to_pod/

/workspace/copy_to_pod
cd /workspace/axolotl
accelerate launch -m axolotl.cli.train /workspace/copy_to_pod/config.yml