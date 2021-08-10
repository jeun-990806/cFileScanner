#!/bin/sh

SOURCE_PATH='.'
DESTINATION_PATH='.'

COMMAND="import headerFileScanner;"

if [ $# -eq 0 ] ; then
	echo -e "opt:\t-sc=[DESTINATION]\tscan symbolic constants and save to [DESTINATION].\n\t-st=[DESTINATION]\tscan structures and save to [DESTINATION].\n\t-set=[SOURCE]\t\tset the path where the header files exist to [SOURCE] (default: ${PWD##*/})"
	echo -e "(the amount of result files can be huge. so it is recommended that you enter the destination path.)" 

else
	for arg in $*
	do
		if [ "${arg%%=*}" == "-set" ] ; then
			SOURCE_PATH="${arg#*=}"
			break
		fi
	done
	COMMAND="${COMMAND} scanner = headerFileScanner.HeaderFileScanner(path='${SOURCE_PATH}');"
	for arg in $*
	do
		if [ ${arg%%=*} == '-sc' ] ; then
			DESTINATION_PATH=${arg#*=}
			COMMAND="${COMMAND} scanner.scanSymbolicConstants(destination='$DESTINATION_PATH');"
		fi
		if [ ${arg%%=*} == '-st' ] ; then
			DESTINATION_PATH=${arg#*=}
			COMMAND="${COMMAND} scanner.scanStructures(destination='$DESTINATION_PATH');"
		fi
	done
	echo "$COMMAND"
	python -c "$COMMAND"
fi
