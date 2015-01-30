#!/bin/bash -e

STATUS500="Status 500 internal server error"
STATUS404="Status 404 file not found"


function removeTempDirectory {
  [ -d "$DIR" ] && rm -Rf $DIR
}

function die {
    removeTempDirectory
    printf "$*\n\n" 1>&2
    trap - EXIT
    exit 1
}

#trap die INT #TERM

PDFLATEX=`which pdflatex`
PDFLATEX_OPTIONS="-halt-on-error"
[ -x "$PDFLATEX"  ] || die $STATUS500

DIR=`mktemp -d 2>/dev/null || mktemp -d -t 'cgilatex'`
[ -d "$DIR" ] || mkdir -p $DIR || die $STATUS500

[ -f $PATH_TRANSLATED ] || die $STATUS404

$PDFLATEX -halt-on-error -output-directory=$DIR $PATH_TRANSLATED || \
    die $STATUS500

printf "Content-Type: application/pdf\n\n"
cat $DIR/*.pdf

removeTempDirectory
exit

