from beam import App, Runtime, Image, Volume, Output
import os

# The runtime definition
app = App(
    "fine-tune-mixtral",
    runtime=Runtime(
        cpu=16,
        memory="32Gi",
        gpu="A100",
        image=Image(
            python_version="python3.10",
            # python_packages="requirements.txt",
            commands=[
                "cd axolotl && pip install packaging && pip install -e '.[flash-attn,deepspeed]'"
            ],
        ),
    ),
    volumes=[
        Volume(name="beam_volume", path="./beam_volume"),
    ],
)


# Training
@app.run()
def train_model():
    os.system("accelerate launch -m axolotl.cli.train examples/mistral/config.yml")
