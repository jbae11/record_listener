from distutils.core import setup

VERSION = '0.0.1'
setup_kwargs = {
    "version": VERSION,
    "description": 'Record Listener',
    "author": 'Jin Whan Bae',
    }

if __name__ == '__main__':
    setup(
        name='record_listener',
        packages=["record_listener"],
        **setup_kwargs
        )
