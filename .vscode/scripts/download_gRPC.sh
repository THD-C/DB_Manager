#!/bin/sh

cd "$(git rev-parse --show-toplevel)" || exit 1

curl -s -L -o thdcgrpc.tar.gz \
    https://github.com/THD-C/Protocol/releases/latest/download/thdcgrpc.tar.gz &&
    tar -xzf thdcgrpc.tar.gz &&
    rm thdcgrpc.tar.gz &&
    cp -r thdcgrpc/* . &&
    rm -r thdcgrpc
