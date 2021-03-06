from invoke import task
import datetime

foldername = '{:%Y%m%d}'.format(datetime.date.today())
commit_message = 'Daily push for {0}'.format(foldername)


@task
def convertnb(c):
    c.run('jupyter nbconvert --to script covid.ipynb')


@task
def convertpy(c):
    c.run('ipynb-py-convert covid.py covid.ipynb')


@task
def build(c, bg=False):
    if bg:
        c.run('python covid.py &')
        c.run('python JH_COVID_DATA_ETL.py &')
    else:
        c.run('python covid.py')
        c.run('python JH_COVID_DATA_ETL.py')


@task
def push(c, tag=False, message=''):
    c.run('git add --all')
    if not message:
        message = commit_message
    c.run('git commit -am "{0}"'.format(message))
    if tag:
        c.run('git tag {0}'.format(foldername))
    c.run('git push origin master')


@task
def release(c):
    c.run('zip -j ./Releases/{0}.zip ./Output/{0}/*'.format(foldername))
    c.run('hub release create -o -a ./Releases/{0}.zip -m \"Covid Graphs for {0}\" {0}'.format(foldername))


@task
def daily(c, numbers=''):
    if numbers:
        c.run('echo "{0}" >> ./Data/COVID_Raw.csv'.format(numbers))
    build(c)
    push(c, tag=True)
    release(c)


@task
def clean(c):
    c.run('rm -rf ./Output/{0}'.format(foldername))
    c.run('./Releases/{0}.zip'.format(foldername))


@task
def rescind(c):
    c.run('git tag -d {0}'.format(foldername))
    c.run('git push --delete origin {0}'.format(foldername))
    c.run('hub release delete {0}'.format(foldername))
