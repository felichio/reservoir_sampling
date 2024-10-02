#!/bin/bash

bin=src/main.py

for i in $(seq 1 $1)
do
    python $bin
done
