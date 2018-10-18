FROM amazonlinux:2018.03.0.20180827

# RUN yum repolist all
RUN yum update -y

RUN yum install -y \
    # compilers
    gcc \
    gcc-c++ \
    # utils
    findutils \
    zip \
    pkgconfig
    
RUN yum install -y python36 \
    python36-devel \
    python36-setuptools

WORKDIR /build

# Create VENV and use pip3 to install everything
RUN python3 -m venv --copies lambda_build && \
    chmod +x lambda_build/bin/activate && \
    source lambda_build/bin/activate

RUN source lambda_build/bin/activate && \
    pip3 install --upgrade pip wheel && \
    pip3 install --no-binary requests requests    

# Zip
RUN cd /build/lambda_build/lib/python3.6/site-packages/ && \
    zip -r -9 -q /build/output.zip *

# copy to mounted windows dir
# COPY ./build.sh /build/build.sh
# CMD chmod +x /build/build.sh && /build/build.sh