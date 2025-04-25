#! /usr/bin/env bash

set -ex

run_generate() {
    ./ipc_bga_generator.py "$1" -v
}

for file in size_definitions/*.yaml; do
    run_generate "$file"
done
