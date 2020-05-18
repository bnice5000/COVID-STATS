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
    c.run('zip -j ./Releases/{0}.zip ./Graphics/{0}/*'.format(foldername))

@task
def push(c, docs=False):
    c.run('git add --all')
    c.run('git commit -am {0}'.format(commit_message))
    c.run('git tag {0}'.format(foldername))
    c.run('git push origin master')
    c.run('hub release create -o -a ./Releases/{0}.zip -m \"Covid Graphs for {0}.\" {0}'.format(foldername))
