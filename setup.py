"""
Copyright(C) Venidera Research & Development, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Venidera Development Team <suporte@venidera.com>
"""

import os
import atexit

from setuptools import find_packages, setup
from setuptools.command.install import install


__title__ = 'vsupport'
__dir_name__ = 'vsupport'
__version__ = '1.0.0'
__author__ = 'Venidera Development Team'
__author_email__ = '<suporte@venidera.com>'
__url__ = 'https://github.com/venidera/vsupport.git'
__description__ = 'Pacote para fornecer support aos projetos da Venidera através do Trello.'
__keywords__ = 'venidera miran miran-lt vsupport risk3'
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "Operating System :: Unix",
    "Topic :: Utilities"
]
__license__ = 'Proprietary'
__maintainer__ = 'Venidera Development Team'
__email__ = '<suporte@venidera.com>'
__status__ = 'Development'
__public_dependencies__ = [
    'unidecode',
    'python-dateutil'
]
__private_dependencies__ = [
]

class PostInstallCommand(install):
    """ customizing post-install actions """
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        atexit.register(PostInstallCommand._post_install)

    @staticmethod
    def _post_install():
        # Manually installing dependencies
        for dep in __private_dependencies__:
            if 'github.com' in dep:
                token = os.environ.get(
                    'ACCESS_TOKEN', os.environ.get('GITHUB_ACCESS_TOKEN'))
                GITHUB_BRANCH = os.environ.get(
                    'GITHUB_BRANCH', 'master')
                # Creating prefix dependency urls
                if '{GITHUB_BRANCH}' in dep:
                    dep = dep.replace('{GITHUB_BRANCH}', GITHUB_BRANCH)
                prefix = f"git+https://{token}@{dep}" if token else f"git+ssh://git@{dep}"
                # Installing dependency
                os.system(f"pip install --upgrade {prefix}")
            elif 'bitbucket.org' in dep:
                # Capturing access token
                BITBUCKET_CREDENTIALS = os.environ.get('BITBUCKET_CREDENTIALS', None)
                token = "$(curl --data \"grant_type=client_credentials\" " + \
                    f"https://{BITBUCKET_CREDENTIALS}@bitbucket.org/site/oauth2/access_token " + \
                        "| grep 'access_token' | awk '{print $5}' | cut -c 2-85)" \
                    if BITBUCKET_CREDENTIALS else None
                # Creating prefix dependency urls
                prefix = f"git+https://x-token-auth:{token}@bitbucket.org/venidera" \
                    if token else 'git+ssh://git@bitbucket.org/venidera'
                os.system(f"pip install --upgrade {prefix}/{dep}.git")

        for dep in __public_dependencies__:
            if any([i + '://' in dep for i in ['ssh', 'http', 'https']]):
                os.system('pip install --upgrade %s' % dep)
        # Removing cache and egg files
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')
        os.system('find ' + __dir_name__ + ' | grep -E ' +
                  '"(__pycache__|\\.pyc|\\.pyo$)" | xargs rm -rf')


if __name__ == '__main__':

    # Running setup
    setup(
        name=__title__,
        version=__version__,
        url=__url__,
        description=__description__,
        long_description=open('README.md').read(),
        author=__author__,
        author_email=__author_email__,
        license=__license__,
        keywords=__keywords__,
        packages=find_packages(),
        install_requires=[
            'setuptools==58.4.0',
            'requests',
            'pytz'
        ] + [p for p in __public_dependencies__ if not any(
            [i + '://' in p for i in ['ssh', 'http', 'https']])],
        classifiers=__classifiers__,
        cmdclass={
            'install': PostInstallCommand
        },
        test_suite="tests"
    )
