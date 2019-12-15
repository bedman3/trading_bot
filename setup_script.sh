python3 -m venv venv
source activate_python.sh
pip install -r requirements.txt

git clone https://github.com/arteria/django-background-tasks.git
pip install django-background-tasks/
rm -rf django-background-tasks

sh download_chromedriver.sh