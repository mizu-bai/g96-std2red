#!/bin/bash

rm -rf frames
mkdir frames
cd frames

gmx trjconv -f ../prod.trr -s ../prod.tpr -o prod.g96 -sep -split 1000 <<EOF
0

EOF

cd ..
