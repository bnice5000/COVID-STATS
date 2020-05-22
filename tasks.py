from invoke import task
import datetime

foldername = '{:%Y%m%d}'.format(datetime.date.today())
commit_message = '\"Daily push for {0}\"'.format(foldername)

@task
def convertnb(c, docs=False):
    c.run('jupyter nbconvert --to script covid.ipynb')

@task
def convertpy(c, docs=False):
    c.run('ipynb-py-convert covid.py covid.ipynb')

@task
def build(c, docs=False):
    c.run('ipython covid.py')

@task
def push(c, tag=False, docs=False):
    c.run('git add --all')
    c.run('git commit -am {0}'.format(commit_message))
    if tag:
        c.run('git tag {0}'.format(foldername))
    c.run('git push origin master')

@task
def release(c, docs=False):
    c.run('zip -j ./Releases/{0}.zip ./Graphics/{0}/*'.format(foldername))
    c.run('hub release create -o -a ./Releases/{0}.zip -m \"Covid Graphs for {0}\" {0}'.format(foldername))

@task
def clean(c):
    c.run('rm -rf ./Graphics/{0}'.format(foldername))
    c.run('/Releases/{0}.zip'.format(foldername))

@task
def rescind(c, docs=False):
    c.run('git tag -d {0}'.format(foldername))
    c.run('git push --delete origin {0}'.format(foldername))
    c.run('hub release delete {0}'.format(foldername))
