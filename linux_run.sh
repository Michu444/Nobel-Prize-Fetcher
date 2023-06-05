#!/bin/bash

# Check if the 'requests' library is installed
if ! python3 -c "import requests" >/dev/null 2>&1; then
    echo "The 'requests' library is not installed. Installing now..."
    pip3 install requests
fi

echo
echo

python3 nobel_people_fetcher.py
