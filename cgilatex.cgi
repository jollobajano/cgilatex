#!/bin/bash -e

DIR=`mktemp -d 2>/dev/null || mktemp -d -t 'cgilatex'`
PDFLATEX=`which pdflatex`

function removeTempDirectory {
  [ -d "$DIR" ] && rm -Rf $DIR
}

function die {
    removeTempDirectory
    printf "Content-Type: text/plain\n\n"
    echo "$1" 1>&2
    echo "$@" 1>&2
    trap - EXIT
    exit 1
}

trap die INT #TERM

[ -d "$DIR" ] || mkdir -p $DIR || die "could not make temp dir"
[ -f $PATH_TRANSLATED ] || die "file $PATH_TRANSLATED not found"
OUT=`$PDFLATEX -output-directory=$DIR $PATH_TRANSLATED` || die $OUT

printf "Content-Type: application/pdf\n\n"
cat $DIR/*.pdf

removeTempDirectory
exit

