#!/bin/bash

echo "Prevent kernel from upgrading!"
dpkg -l | grep linux-image | awk '{print $2}' > linux-image.lst
input="$(pwd)/linux-image.lst"
while IFS= read -r image 
do
  echo $image hold | sudo dpkg --set-selections 
done < "$input"
dpkg -l | grep "linux-image"
