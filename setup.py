from setuptools import setup
import os
with open('requirements.txt') as f:
    required = f.read().splitlines()

package_name = 'simulateur_choix'
setup(
    name='simulateur_choix',
    version='0.0.1',
    packages=[package_name],
    package_dir={'': 'src'},
    test_suite = 'test',
    install_requires=required,
    python_requires='>3.10'
)
