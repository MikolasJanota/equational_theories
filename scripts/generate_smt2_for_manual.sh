#!/bin/bash
#
# File:  get_interesting.sh
# Author:  mikolas
# Created on:  Thu Apr 24 10:00:53 CEST 2025
# Copyright (C) 2025, Mikolas Janota
#
#

set -u
odir=cex_manual
mkdir -p ${odir}
for f in ../equational_theories/ManuallyProved/*.lean; do
	if grep -q 'theorem Equation[0-9]\+_not_implies_Equation[0-9]\+' $f; then
		echo $f
		grep 'theorem Equation[0-9]\+_not_implies_Equation[0-9]\+' $f | \
			sed -E 's/.*theorem Equation([0-9]+)_not_implies_Equation([0-9]+).*/\1 \2/' |\
			while read  eqs; do
				e1=`echo "${eqs}" | cut -f1 -d' '`
				e2=`echo "${eqs}" | cut -f2 -d' '`
				echo $e1 '-->' $e2
				python3 generate_smt2.py -i $e1 $e2 >${odir}/cex_int_${e1}_${e2}.smt2
				python3 generate_smt2.py $e1 $e2 >${odir}/cex_uns_${e1}_${e2}.smt2
			done
	fi
done

