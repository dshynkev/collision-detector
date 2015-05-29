#!/bin/bash

for i in *.py; do
	if grep -q -i 'LAST EDIT' ${i}; then
		touch -r ${i} __stamp
		mod_date=$(stat ${i} -c '%.19y')
		sed -i.bak -e "s/LAST\ EDITED:.*/LAST\ EDITED:\t${mod_date}/" ${i}
		touch -r __stamp ${i}
	fi
done

if [ -e __stamp ]; then
	rm __stamp;
fi
