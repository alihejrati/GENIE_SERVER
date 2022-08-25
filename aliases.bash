#!/bin/bash

# app install
alias ierd="apt install graphviz && apt install graphviz-dev && pipenv install pyparsing pydot && pipenv install django-extensions"

# dbms
alias dbmsmysqlup="systemctl start mysql.service"

# git
alias ga="git add ."
alias gc="git commit -m "
alias gcc="git commit --amend -m "
alias g="ga && gc"
alias gg="ga && gcc"               # arg1: commit_msg
alias gp="git push"
alias gpull="git pull"
alias gl="git log"
alias gl1="git log --oneline"
alias glt="git log --branches --remotes --tags --graph --oneline --decorate"
alias glr="git remote -v"
alias gr1="git reset --hard HEAD~1"
alias gb="git checkout "           # arg1: branch_name
alias gbf="git checkout -b"        # arg1: new_branch_name, arg2: hash_name 0f this branch
alias gbv="git branch -v"          # show all local branche names 
alias gbva="git branch -a"         # show all branche
alias gbd="git branch -d "         # arg1: branch_name
alias gbD="git branch -D "         # arg1: branch_name
alias gbds="git push -d "          # arg1: server_name(example:origin) arg2: branch_name_on_server
alias grs="git reset --soft "      # arg1: hash_name
alias grh="git reset --hard "      # arg1: hash_name
alias gt="ssh -T git@gitlab.com"
gmerge() {
    echo $(grh $1 && gcc $2) 
}

# django basic
alias pm="python manage.py"
alias pmcs="python manage.py collectstatic --noinput"
alias pmdbsh="python manage.py dbshell"
alias pmdd="python manage.py dumpdata"
alias pmld="python manage.py loaddata"
alias pmm="python manage.py migrate"
alias pm2m="python manage.py makemigrations"
alias pmmg="pm2m && python manage.py migrate"
alias pmsh="python manage.py shell"
alias pmsm="python manage.py schemamigration"
alias pmsync="python manage.py syncdb --noinput"
alias pmt="python manage.py test"
alias pmrs="python manage.py runserver"
alias pmsm="python manage.py sqlmigrate auth 0001" # TODO: try to define a function for this
pmsql() {
    echo $(python manage.py makemigrations $1 --empty) 
}
pmseed() {
    echo $(python manage.py seed $1 --number=$2) 
}

# os
alias mkp="mkdir -p"

# documentation
alias pmerddot="python manage.py graph_models -a > documentation/ERD.dot"
alias pmerd="pmerddot && python manage.py graph_models --pydot -a -g -o documentation/ERD.png"
alias doc="mkp documentation && pmerd"