#!/bin/bash

gmx grompp -f prod.mdp -c eq.gro -p topol.top -o prod.tpr -maxwarn 114514
gmx mdrun -v -deffnm prod
