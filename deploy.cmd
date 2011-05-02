#!/bin/bash
#if ["$1" == ""]; then
#	echo "Usage: bash t/deploy1.cmd NNN  (NNN=version number)"
#else
#	appcfg.py update -V r$1 appengine/
	appcfg.py update -V 2 appengine/
#fi
