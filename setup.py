import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package]) 

def install_packages():
    packages = ['bs4', 'python-nmap', 'asyncio', 'socket', 'optparse']
    for p in packages:
        import_or_install(p)

install_packages()