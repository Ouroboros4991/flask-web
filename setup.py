from setuptools import find_packages, setup

setup(
    name='Text to speech API',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'flask',
        'google-api-python-client>=1.7.3',
        'google-cloud-speech>=0.34.0'
    ],
)
