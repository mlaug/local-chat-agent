# Add vscode user for Jetson-compatible PyTorch 2.6.0 container with audio/video support

FROM nvcr.io/nvidia/pytorch:24.12-py3-igpu

ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_VERSION=12.6
ENV TORCH_VERSION=2.6.0

# Create vscode user
RUN useradd -ms /bin/bash vscode && \
    usermod -aG sudo vscode

# Install system packages
RUN apt-get update && \
    apt-get install -y \
    sudo \
    wget \
    git \
    build-essential \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libavdevice-dev \
    libavutil-dev \
    libasound2-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libsndfile1 \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    python3-pyaudio \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Optional: cuSPARSELt for PyTorch 2.6+
RUN wget https://raw.githubusercontent.com/pytorch/pytorch/5c6af2b583709f6176898c017424dc9981023c28/.ci/docker/common/install_cusparselt.sh && \
    bash install_cusparselt.sh && \
    rm install_cusparselt.sh

# Install PyTorch 2.6.0 for JetPack 6.0
RUN wget https://developer.download.nvidia.com/compute/redist/jp/v60dp/pytorch/torch-2.6.0+nv24.12-cp310-cp310-linux_aarch64.whl && \
    pip install torch-2.6.0+nv24.12-cp310-cp310-linux_aarch64.whl && \
    rm torch-2.6.0+nv24.12-cp310-cp310-linux_aarch64.whl

# Install supporting libraries
RUN pip install --no-cache-dir \
    torchvision \
    torchaudio \
    opencv-python-headless \
    pyaudio

# Set default user
USER vscode

CMD [ "bash" ]
