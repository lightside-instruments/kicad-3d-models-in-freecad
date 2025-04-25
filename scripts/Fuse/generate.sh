#! /usr/bin/env bash

set -ex

run_generate() {
    ./ptc-fuse-tht.py "$1" -v
}

for file in size_definitions/*.yaml; do
    run_generate "$file"
done
