#!/bin/bash
br=`brillo -G | awk -F"." '{ print $1 }'`
echo "$br%"
