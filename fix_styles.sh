./make_style.sh
echo "yes" | /envs/dmoj/bin/python manage.py collectstatic
/envs/dmoj/bin/python manage.py compilemessages
/envs/dmoj/bin/python manage.py compilejsi18n
/envs/dmoj/bin/python manage.py loaddata navbar
/envs/dmoj/bin/python manage.py loaddata language_small
