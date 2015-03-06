from metamake import task, shell, path, bootstrap, list_tasks

bootstrap("Makefile")
MODULENAME = "rython"

@task(default=True)
def ls():
    """shows all available tasks"""
    list_tasks()

@task
def build():
    """builds everything into a source distribution"""
    shell("python setup.py sdist")

@task
def install():
    """installs the latest built module"""
    tarballs = sorted(path("dist").listdir("*.tar.gz"))
    if not tarballs:
        build()
        tarballs = sorted(path("dist").listdir("*.tar.gz"))
    latest = tarballs[-1]
    shell("easy_install --upgrade %s" % latest)

@task
def release():
    """releases this code + documentation to pypi"""
    shell("python setup.py register")
    shell("python setup.py sdist upload")

@task
def clean():
    """cleans all intermediate files"""
    if path("MANIFEST").exists():
        path("MANIFEST").remove()
    if path("build").exists():
        path("build").rmtree()
    if path("dist").exists():
        path("dist").rmtree()
    patterns = ["*.coverage", "*.sqlite", "*.csv", "*.prof", "*.egg-info", "*.so", "*.dll", "*.c", "*.pyc"]
    def recursive_remove_pyc(p):
        for f in p.listdir("*"):
            if f.isdir():
                recursive_remove_pyc(f)
            elif f.endswith(".pyc"):
                f.remove()
    recursive_remove_pyc(path("."))
    for p in patterns:
        for d in [".", "tests", MODULENAME]:
            if path(d).exists():
                for f in path(d).listdir(p):
                    if f.isdir():
                        f.rmtree()
                    else:
                        f.remove()