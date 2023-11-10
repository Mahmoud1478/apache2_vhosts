from setuptools import setup
setup(
    name='domains',
    version='0.1',
    author='Mahmoud Mostafa Ali',
    author_email='mah.mostafa18@gmail.com',
    platforms='Linux Debian based',
    license='MIT',
    description='''this script helps you to automate the setup steps when add new domain to your apache2 web server ''',
    home_page='mahmoud-mostafa.com',
    py_modules=[
        'main'
    ],
    install_requires=[
        'click'
    ],
    entry_points='''
        [console_scripts]
        hosts=main:main   
    '''
)
