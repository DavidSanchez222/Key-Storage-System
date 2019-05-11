from setuptools import setup

setup(
    name = 'kss',
    version = 2.0,
    py_modules = ['kss'],
    install_requires = [
        'Click',
        'Tabulate',
        'python-dotenv'
    ],
    entry_points = '''
        [console_scripts]
        kss = kss:cli
        ''',
)