from setuptools import setup

setup(
    name = 'kss',
    version = 0.1,
    py_modules = ['kss'],
    install_requires = [
        'Click',
        'Tabulate',
        'Dotenv'
    ],
    entry_points = '''
        [console_scripts]
        kss = kss:cli
        ''',
)