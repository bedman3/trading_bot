mkdir -p downloads
wget -q https://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_linux64.zip -O downloads/chromedriver.zip
unzip -o downloads/chromedriver.zip -d downloads/
rm downloads/chromedriver.zip