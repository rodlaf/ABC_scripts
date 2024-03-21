## Fine-tuning an LLM (Mixtral) on CAD Data for Text-to-CAD

The goal of this repo is to train Mixtral on the ABC dataset in order to get it to 
generate correct CAD models in the form of .STEP files. 

The steps required to get this to work are to:

1) Be selective about the data. It is a lot and I am not sure how long the fine tuning 
process will take on the GPUs I have at my disposal.

2) Format the data in the correct format. E.g., instruction, prompt, output JSON format.

3) Pick and execute the correct model to work on. Mixtral is only one option. I have 
also looked at this link: https://github.com/stochasticai/xturing.

### ABC Dataset

* This thing is huge and it will most likely have to be very cherry picked to fine tune 
anything in a reasonable amount of time.
* It is split into 100 chunks. Each has 10k data points. Downloading even one chunk 
takes a fast computer with fast internet about 20 minutes. 

### Immediate TODOs:

* Create a Python script that pulls a chunk of the ABC dataset.
    - TODO: Finish
    
* Create a Python script that formats ABC chunk into usable finetuning data.

* AGGREGATE all chunks into one chunk before doing finetuning