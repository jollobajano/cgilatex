# cgilatex

## Apache serving LaTeX files as rendered PDFs using a Bash script handler

I thought I'd start logging my daily [geekie] explorations. This is first time out so bear with me.

I had this idea for years. To have apache render LaTeX files as rendered PDF files. Many have had the idea but their often met by objections that the Tex family programs use and produce files beside the rendered file.

I'm using

	+ Apache web server.
	+ Bash as the script engine.
	+ LaTeX as my renderer. I could make this fancier by grep'ing the .tex file for clues like "\documentclass" and "\usepackage{fontspec}" but this is just a PoC and not a full-fledged technical sollutio.

My solution builds on
	+ A LaTeX rendering CGI script.
	+ Some Apache configuration.
	+ Using the *nix mktemp command and LaTeX's --output-directory option for the rendering.
	+ 
In my daily doings I' a Java-ist by birth and a terrible Bash'er so comments on my scripting style are probably justifies.

I had to check up on error-handling, the old HTTP environment variables as well as bash file tests and more.

The bash script goes, however, as follows:

  #!/bin/bash -e

  DIR=`mktemp -d 2&gt;/dev/null || mktemp -d -t 'cgilatex'`
  PDFLATEX=`which pdflatex`

  function removeTempDirectory {
    [ -d "$DIR" ] &amp;&amp; rm -Rf $DIR
  }

  function die {
    removeTempDirectory
    printf "Content-Type: text/plain\n\n"
    echo "$1" 1&gt;&amp;2
    echo "$@" 1&gt;&amp;2
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

The extra Apache configuration to let the web server serve .tex files through the bash script is done locally for this project but could just as well have been made globally in the httpd.conf.
  <Directory "/Users/mats/Sites/cgilatex">
    Options +Indexes +ExecCGI
    DirectoryIndex index.cgi
    AddHandler cgi-script .cgi

    Action pdflate-action /cgilatex/cgilatex.cgi
    AddHandler pdflate-action .tex
  </Directory>

The example LaTeX document was a hand crafted Ipsum and goes something like this

  \documentclass[a4paper,12pt]{article}
  \title{CGILatex}
  \author{Mats Nyberg}
  \begin{document}
    \maketitle

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut
    aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum."

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut
    aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum.
  \end{document}


#### References

http://linuxcommand.org/wss0150.php

http://linuxcommand.org/wss0160.php

http://tldp.org/LDP/abs/html/fto.html
