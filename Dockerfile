# copied from axolotl repo

ARG CUDA_VERSION="11.8.0"
ARG CUDNN_VERSION="8"
ARG UBUNTU_VERSION="22.04"
ARG MAX_JOBS=4

FROM nvidia/cuda:$CUDA_VERSION-cudnn$CUDNN_VERSION-devel-ubuntu$UBUNTU_VERSION as base-builder

ENV PATH="/root/miniconda3/bin:${PATH}"

ARG PYTHON_VERSION="3.10"
ARG PYTORCH_VERSION="2.1.2"
ARG CUDA="118"
ARG TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6 9.0+PTX"

ENV PYTHON_VERSION=$PYTHON_VERSION
ENV TORCH_CUDA_ARCH_LIST=$TORCH_CUDA_ARCH_LIST

# install python

RUN apt-get update \
    && apt-get install -y wget git build-essential ninja-build git-lfs libaio-dev && rm -rf /var/lib/apt/lists/* \
    && wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && conda create -n "py${PYTHON_VERSION}" python="${PYTHON_VERSION}"

ENV PATH="/root/miniconda3/envs/py${PYTHON_VERSION}/bin:${PATH}"

WORKDIR /workspace

# install torch

RUN python3 -m pip install --upgrade pip && pip3 install packaging && \
    python3 -m pip install --no-cache-dir -U torch==${PYTORCH_VERSION}+cu${CUDA} --extra-index-url https://download.pytorch.org/whl/cu$CUDA

# install axolotl

RUN git clone --depth=1 https://github.com/OpenAccess-AI-Collective/axolotl.git
WORKDIR /workspace/axolotl
RUN pip3 install -e '.[flash-attn,deepspeed]'

# copies my data over

RUN apt-get install -y vim screen htop
WORKDIR /workspace
COPY ./copy_to_pod ./copy_to_pod

# fine tune
# MUST USE `docker run --gpus '"all"' abcft`

CMD bash /workspace/copy_to_pod/fine-tune.sh