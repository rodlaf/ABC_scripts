import subprocess
from beam import App, Runtime, Image, Volume, Output
import os

# The runtime definition
app = App(
    "fine-tune-mixtral",
    runtime=Runtime(
        cpu=16,
        memory="16Gi",
        # gpu="A10G",
        image=Image(
            python_version="python3.10",
            python_packages="requirements.txt",
            commands=["apt-get update && apt-get install -y wget p7zip-full p7zip-rar"],
        ),
    ),
    volumes=[
        Volume(name="dataset", path="./dataset"),
    ],
)


# Training
@app.run(outputs=[Output(path="output.log")])
def train_model():
    os.system("chmod +x ./scripts/download_dataset.sh")
    os.system("./scripts/download_dataset.sh > output.log 2>&1")
