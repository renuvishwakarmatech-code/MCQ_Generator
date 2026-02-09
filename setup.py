from setuptools import setup, find_packages

setup(
    name='mcq_generator',
    version='0.1.0',
    author='Renu Vishwakarma',
    author_email='renu.vishwakarma.tech@gmail.com',
    packages=find_packages(),
    install_requires=[
        'groq',
        'langchain',
        'streamlit',
        'python-dotenv',
        'PyPDF2'
    ]
)