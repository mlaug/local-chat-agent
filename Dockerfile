# Jetson-compatible PyTorch 2.7.1 with audio and vision support (CUDA 12.6, Ubuntu 24.04)
FROM nvcr.io/nvidia/l4t-jetpack:r36.4.0

ENV DEBIAN_FRONTEND=noninteractive
ENV TORCH_VERSION=2.7.1
ENV TORCH_AUDIO_VERSION=2.7.1
ENV TORCH_VISION_VERSION=0.22.0
ENV TORCH_CUDA_ARCH_LIST="8.7"
ENV CUDA_HOME=/usr/local/cuda
ENV TORCH_USE_XCCL=0
ENV PATH="/home/vscode/.local/bin:$PATH"

# Create user
RUN useradd -ms /bin/bash vscode
USER vscode
WORKDIR /home/vscode

# Install dependencies (system + build + Python)
USER root
RUN apt-get update && \
    apt-get install -y wget git cmake ninja-build build-essential curl gnupg \
    ffmpeg libavcodec-dev libavformat-dev libswscale-dev libavdevice-dev libavutil-dev \
    libasound2-dev libglib2.0-0 libsm6 libxext6 libxrender-dev \
    libsndfile1 libportaudio2 libportaudiocpp0 portaudio19-dev python3-pyaudio \
    libopenblas-dev libblas-dev m4 libffi-dev libssl-dev python3-dev python3-pip \
    libjpeg-dev zlib1g-dev libpng-dev python3-venv python3-typing-extensions \
    unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python upgrades
USER vscode
RUN pip3 install --upgrade pip && \
    pip3 install "numpy>=2.0.0"

# Clone and build PyTorch
RUN git clone --recursive https://github.com/pytorch/pytorch && \
    cd pytorch && \
    git checkout v${TORCH_VERSION} && \
    git submodule sync && git submodule update --init --recursive && \
    pip3 install -r requirements.txt && \
    USE_CUDA=1 TORCH_CUDA_ARCH_LIST=${TORCH_CUDA_ARCH_LIST} CUDA_HOME=${CUDA_HOME} \
    CMAKE_PREFIX_PATH=$(python3 -c "from sysconfig import get_paths as gp; print(gp()['purelib'])") \
    python3 setup.py bdist_wheel && \
    pip3 install dist/*.whl

# Clone and build TorchVision
RUN git clone --recursive https://github.com/pytorch/vision && \
    cd vision && \
    git checkout v${TORCH_VISION_VERSION} && \
    git submodule sync && git submodule update --init --recursive && \
    python3 setup.py bdist_wheel && \
    pip3 install dist/*.whl

# Clone and build TorchAudio
RUN git clone --recursive https://github.com/pytorch/audio && \
    cd audio && \
    git checkout v${TORCH_AUDIO_VERSION} && \
    git submodule sync && git submodule update --init --recursive && \
    python3 setup.py bdist_wheel && \
    pip3 install dist/*.whl

WORKDIR /home/vscode

CMD [ "bash" ]
