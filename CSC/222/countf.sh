#!/bin/bash

directories=()
filenames=()
fcount=0
dcount=0
dirmode=true #unused currently
filemode=true # unused currently

function pushdir
{
	
	pushd "$@" > /dev/null

}

function popdir
{
	
	popd "$@" > /dev/null

}

#checks if the argument matches any of the patterns given by -f
function pmatch
{

	for pat in "${filenames[@]}"
	do
		case "$1" in
			*"$pat"*) echo test && return 0 ;;
		esac
	done
	return 1

}

#main logic
function countf
{
	#go into arg directory
	pushdir "$1"
	for f in *
	do
		#recurse for directories
		if [ -d "$f" ]
		then
			if [ $(pmatch "$f") ] || [ "${#filenames[@]}" -eq 0 ]
			then
				dcount=$((dcount + 1))
			fi
			countf "$f"
		else
			#check if patterns specified
			if [ "${#filenames[@]}" -gt 0 ]
			then
				if [ $(pmatch "$f") ]
				then
					fcount=$((fcount +1))
				fi
			else
				fcount=$((fcount + 1))
			fi
		fi
	done
	#leave arg directory
	popdir

} 

#argument parsing
if [[ "$@" =~ "-h" ]] # skip process if -h flag is present
then
	echo USAGE: sh countf.sh '[DIRECTORIES]...' '[OPTIONS]...'	
	echo Recursively calculates the total number of files and directories in given directories
	echo If no directories are specified, the crawl starts at the current working directory
	echo
	echo Options:
	echo -e '\t' -h '\t': show this menu
	echo -e '\t' -p '[PATTERN]''\t': restrict count to specific file names
	echo -e '\t\t' sh countf.sh dir1 dir2 -p file1 -p file2
else
	#differentiate directory and file pattern arguments
	while [ $# -gt 0 ]
	do
		if [[ "$1" == "-p" ]]
		then
			shift
			filenames+=( "$1" )
		else
			directories+=( "$1" )
		fi
		shift
	done
fi
#run main logic
if [ ${#directories[@]} -gt 0 ]
then
	for dir in ${directories[@]}
	do
		countf $dir
	done
else
	countf ./
fi

#result
echo TOTAL: $((dcount + fcount))
echo DIRECTORIES: $dcount
echo FILES: $fcount
 

