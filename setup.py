from setuptools import setup, find_packages

setup(
    name='invoice_gettor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'asyncio',
        'playwright',
        'OpenAI',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'invoice_gettor = invoice_gettor.cli:cli',
        ],
    },
)