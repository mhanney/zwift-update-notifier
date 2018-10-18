# Build Python libraries for Amazon Linux Lambda using Docker

This project uses Docker to compile Python libraries for use in the Amazon Lambda Linux environment. 

## How to use

Install Docker

Clone this repo and cd into it from a shell.

## Build the docker image

Run the following command from the root of this project. This will create a docker image called `docker-build-lambda-py-libs` using the commands in the `Dockerfile`

```
docker build -t docker-build-lambda-py-libs .
```


## Then run the docker image manually (Windows)

This will run `amazonlinux:latest` docker image and mount `C:/Users/mhanney/dev/zwift-update-notifier/lib:/outputs` as `/outputs` inside the docker image.

```
docker run -v C:/Users/mhanney/dev/zwift-update-notifier/lib:/outputs -it docker-build-lambda-py-libs:latest
```

Now you should be able to cd to ./outputs in this project root and see the build python libraries zip file. Copy it to your Python Lambda project ready to deploy to Amazon Lambda.

```
cp -R /build/*.zip /outputs
```


## To Rebuild without cache

You should only need to do this if you run into problems
```
docker build --no-cache=true -t docker-build-lambda-py-libs .
```

