#!/bin/bash

if [[ $1 == "t" ]]; then
  date "+%R"
else
  date "+%a %d %b"
fi
