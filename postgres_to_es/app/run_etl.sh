#!/bin/sh

cd data_to_db && python main.py && cd .. && cd data_to_es && python main.py && cd ..
