#!/bin/bash

for i in *.py; do
	if grep -q -i 'LAST EDIT' ${i}; then
		stat ${i} -c '%.19y'
	fi
done
