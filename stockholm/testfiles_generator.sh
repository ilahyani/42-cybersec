#!/bin/bash

extensions=("docx" "xlsx" "jpg" "pdf" "txt")

for i in {1..10}; do
    ext="${extensions[$((RANDOM % ${#extensions[@]}))]}"
    filename="$HOME/infection/file_${i}.$ext"
    echo "This is a dummy file for testing." > "$filename"
    echo "Created $filename with dummy content."
    done