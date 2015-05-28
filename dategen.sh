#!/bin/bash

for i in *.py; do
	if grep -q -i 'LAST EDIT' ${i}; then
		mod_date=$(stat ${i} -c '%.19y')
		sed -i.bak -e "s/LAST\ EDITED:*/LAST\ EDITED:\t${mod_date}/" ${i}
	fi
done
