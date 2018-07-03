cd /root/water_com

git fetch origin
git merge origin/master

pip3 install -r requirements.txt

cd /root/water_com/water_com

python3 manage.py migrate --settings=water_com.settings_prod
python3 manage.py collectstatic --no-input --settings=water_com.settings_prod

supervisorctl restart water_com
service nginx restart