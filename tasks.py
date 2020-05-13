from invoke import task

@task
def build(c, docs=False):
    c.run("jupyter nbconvert --to script covid.ipynb")
