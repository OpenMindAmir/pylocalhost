# In the name of Allah

import os,sys,atexit,time,shutil,json
from distutils.dir_util import copy_tree

colors = {
    'RED':'\033[1;31m',
    'GREEN':'\033[1;32m',
    'YELLOW':'\033[1;33m',
    'MAGENTA':'\033[1;35m',
    'BLUE':'\033[1;34m',
    'CYAN':'\033[1;36m',
    'WHITE':'\033[1;37m'
}

info = {'python':None,'license_accepted':False,'installtion_complete':False,'username':None,'home':None}

sys.stdout.write(colors['MAGENTA'])
print('In the name of Allah\n')
time.sleep(2)

sys.stdout.write(colors['YELLOW'])
print('MWX\nmwxgaf.ir\nTwitter: @mwxgaf\n')
time.sleep(2)

print('PyLocalhost\n')
time.sleep(2)

# Making atexit function
def end():
    if not info['installtion_complete']:
        sys.stdout.write(colors['YELLOW'])
        print('\nInstaller exited from installtion process and resault was not successfull!\nIf you have an issue please submit it at Github repository of project:\nhttps://github.com/mwxgaf/pylocalhost\n')
    else:
        sys.stdout.write(colors['GREEN'])
        print('\nSaving your system info ...')
        info_json_file = open('info.json','w')
        json.dump(info,info_json_file)
        print('\nInstalltion completed successfully\nThank you for using Pylocalhost :)')
atexit.register(end)

# Asking user for accepting the license
sys.stdout.write(colors['CYAN'])
print('This software is licensed under MPL-2.0\n(Mozilla public license - version 2.0)\n')
while not info['license_accepted']:
    sys.stdout.write(colors['YELLOW'])
    accept_question = input('Do you agree with the license (y/n)? ')
    print('\n')
    if accept_question.lower() == 'y':
        info['license_accepted'] = True
    elif accept_question.lower() == 'n':
        sys.stdout.write(colors['RED'])
        print('You must be agree with license to install and use this software!\n')
        sys.exit(406)
    else:
        continue


# Check if OS is supported or not
if os.name == 'nt':
    sys.stdout.write(colors['RED'])
    print('Microsoft Windows OS is not supported yet!')
    sys.exit(400)
sys.stdout.write(colors['GREEN'])
print('Operating system supported! Starting dependencies installtion check ...\n')

# Check if dependencies are installed or not
def check_installtion(package):
    if not os.popen('which {}'.format(package)).read().startswith('/'):
        sys.stdout.write(colors['RED'])
        print('Clound not detect {} installtion!'.format(package))
        sys.exit(404)
    sys.stdout.write(colors['CYAN'])
    print('{} installtion found! ...'.format(package))

for p in ['nginx','git','wget']:
    check_installtion(p)
sys.stdout.write(colors['GREEN'])
print('Checking completed successfully!\n')

# Checking and finding python 3
for p in ['python3 --version','python --version']:
    if os.popen(p).read()[7] == '3':
        info['python'] = p.split()[0]
if not info['python']:
    sys.stdout.write(colors['RED'])
    print('Could not find python version 3 in your system!')
    sys.exit(404)
sys.stdout.write(colors['GREEN'])
print('Python version 3 found! Starting installtion ...\n')

# Installing virtualenv
sys.stdout.write(colors['CYAN'])
print('Installing virtualenv ...')
try:
    venv_setup = os.popen('sudo -H {} -m pip install virtualenv'.format(info['python']))
    os.waitpid(venv_setup._proc.pid,0)
except BrokenPipeError:
    pass
check_installtion('virtualenv')

# Initializing venv
def unknown_error(e):
    sys.stdout.write(colors['RED'])
    print('Unknown error: {}\n'.format(e))
    sys.exit(500)
def permission_error():
    sys.stdout.write(colors['RED'])
    print('Not enough permissions! run file with sudo\n')
    sys.exit(403)

sys.stdout.write(colors['CYAN'])
print('Creating main directory ...\n')

try:
    os.chdir('/etc/')
except FileNotFoundError:
    sys.stdout.write(colors['RED'])
    print('Seems that your operating system is not supported!\n')
    sys.exit(404)
except Exception as e:
    unknown_error(e)

tries = 5
def make_main_dir(tries):
    try:
        os.mkdir('./pylocalhost')
    except FileExistsError:
        if tries != 0:
            try:
                shutil.rmtree('./pylocalhost')
            except PermissionError:
                permission_error()
            except Exception as e:
                unknown_error(e)
            tries -= 1
        else:
            unknown_error('Could not make main directory!\n')
        make_main_dir(tries)
    except PermissionError:
        permission_error()
    except Exception as e:
        unknown_error(e)
make_main_dir(tries)

os.chdir('/etc/pylocalhost')
sys.stdout.write(colors['CYAN'])
print('Initializing virtual enviroment ...\n')

venv_init = os.popen('sudo {} -m virtualenv .venv'.format(info['python']))
os.waitpid(venv_init._proc.pid,0)

if not os.path.isfile('/etc/pylocalhost/.venv/bin/python'):
    unknown_error('Could not initialize virtual envirpment\n')

print('Cloning software from Github ...')

git_proccess = os.popen('sudo git clone https://github.com/mwxgaf/pylocalhost.git temp')
os.waitpid(git_proccess._proc.pid,0)
copy_tree('/etc/pylocalhost/temp','/etc/pylocalhost')
shutil.rmtree('/etc/pylocalhost/temp')

if not os.path.isfile('/etc/pylocalhost/app.py'):
    unknown_error('\nCloud not clone git repository successfully!')

print('Downloading Jquery ...')
os.chdir('/etc/pylocalhost/static/script')
jquery_download = os.popen('wget https://code.jquery.com/jquery-3.5.1.min.js')
os.waitpid(jquery_download._proc.pid,0)
os.chdir('/etc/pylocalhost')

if not os.path.isfile('/etc/pylocalhost/static/script/jquery-3.5.1.min.js'):
    unknown_error('\nCould not Download Jquery!')

print('Installing dependencies ...')

try:
    req_install_porcess = os.popen('sudo -H /etc/pylocalhost/.venv/bin/pip install -r requirements.txt')
    os.waitpid(req_install_porcess._proc.pid,0)
except BrokenPipeError:
    pass

if not os.path.isfile('/etc/pylocalhost/.venv/bin/gunicorn'):
    unknown_error('\nCould not install dependencies!')

# Create and write Nginx and Gunicorn config file
print('Configuring your system ...')

info['home'] = os.popen('echo $HOME').read()[:-1]
info['username'] = info['home'].split('/')[2]

os.chdir(info['home'])
os.makedirs('Pylocalhost',exist_ok=True)
shutil.chown(os.path.join(info['home'],'Pylocalhost'),user=info['username'])
os.popen('sudo chmod ug=rwx,o=rx Pylocalhost/')
os.chdir('/etc/pylocalhost')

pylocalhost_file = open('/etc/nginx/sites-available/pylocalhost','w')
pylocalhost_file.write('server {\n    listen 80 default_server;\n    listen [::]:80;\n    root %s/Pylocalhost;\n    server_name localhost;\n    location /static {\n        alias /etc/pylocalhost/static;\n    }\n    location /s {\n        alias %s/Pylocalhost;\n    }\n    location / {\n        try_files $uri @wsgi;\n    }\n    location @wsgi {\n        proxy_pass http://unix:/tmp/gunicorn.sock;\n        include proxy_params;\n    }\n}' % (info['home'],info['home']))
pylocalhost_file.close()

gunicorn_file = open('/etc/systemd/system/gunicorn.service','w')
gunicorn_file.write('[Unit]\nDescription=gunicorn daemon for Pylocalhost\nAfter=network.target\n\n[Service]\nUser={}\nGroup=www-data\nRuntimeDirectory=gunicorn\nWorkingDirectory=/etc/pylocalhost/\nExecStart=/etc/pylocalhost/.venv/bin/gunicorn --bind=unix:/tmp/gunicorn.sock --workers=2 app:app\nExecReload=/bin/kill -s HUP $MAINPID\nExecStop=/bin/kill -s TERM $MAINPID\n\n[Install]\nWantedBy=multi-user.target'.format(info['username']))
gunicorn_file.close()

shutil.move('/etc/nginx/nginx.conf','/etc/nginx/nginx.conf.default')
shutil.copy('/etc/pylocalhost/nginx.conf','/etc/nginx/nginx.conf')

try:
    os.remove('/etc/nginx/sites-enabled/default')
except FileNotFoundError:
    pass

try:
    os.remove('/etc/nginx/sites-enabled/pylocalhost')
except FileNotFoundError:
    pass

os.chdir('/etc/nginx/sites-enabled')
os.symlink('/etc/nginx/sites-available/pylocalhost')

print('Reloading Systemctl daemon ...')

daemon_reload = os.popen('sudo systemctl daemon-reload')
os.waitpid(daemon_reload._proc.pid,0)

print('Finalizing installtion ...')

time.sleep(2)
info['installtion_complete'] = True

sys.stdout.write(colors['GREEN'])
print('\nDone! :)')

sys.exit(0)