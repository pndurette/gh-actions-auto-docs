#!/bin/bash

# Replace the lines between <!--doc_begin-->
# and <!--doc_end--> in $1 with the contents of $2.
# Outputs to stdout.

if [[ $# -ne 2 ]]; then
    echo "Illegal number of parameters" >&2
    echo "usage: $0 <file to replace in> <replacement file>"
    exit 1
fi

# Temp file
TEMP_FILE=$(mktemp)

# Delete everything between anchors (exclusive)
# https://stackoverflow.com/a/10271732
sed '/<!--doc_begin-->/,/<!--doc_end-->/{//!d;}' $1 > $TEMP_FILE

# Inserts contents of $1 file immediatly after first anchor
# ($2 file needs a newline, otherwise the closing anchor won't be on a newline)
# https://stackoverflow.com/a/2512379
sed "/<!--doc_begin-->/r $2" $TEMP_FILE

# Cleanup
rm $TEMP_FILE