### PYTHON PACAKGE
echo 'Installing python packages'
pip install -r requirements.txt


### GECKODRIVER
echo 'Getting geckodriver'
get_latest_release() {
	curl --silent "https://api.github.com/repos/$1/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
}

NAME=geckodriver
TAR=$NAME.tar.gz
RELEASE=$(get_latest_release "mozilla/geckodriver")

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    if $(uname -a | grep 'x86_64'); then
		OS=linux32
	else
		OS=linux64
	fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
	OS=macos
else
	echo "Error: unknown os type" 
    exit
fi

URL="https://github.com/mozilla/geckodriver/releases/download/$RELEASE/geckodriver-$RELEASE-$OS.tar.gz"

curl -o $TAR -L $URL
tar -xf $TAR
rm $TAR
