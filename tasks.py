from invoke import task
import datetime

@task
def convertnb(c, docs=False):
    c.run('jupyter nbconvert --to script covid.ipynb')

def convertpy(c, docs=False):
    c.run('ipynb-py-convert covid.py test.ipynb')

@task
def build(c, docs=False):
    c.run('ipython covid.py')

@task
def push(c, docs=False):
    c.run('git add .')
    commit_message = '\"Daily push for {:%Y%m%d}\"'.format(datetime.date.today())
    c.run('git commit -m {0}'.format(commit_message))
    c.run('git push origin master')
