import codecs
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as file:
    long_description = file.read()


def read(rel_path):
    with codecs.open(os.path.join(here, rel_path), "r") as file:
        return file.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


version = get_version("src/rsaidnumber/__init__.py")


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version."""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")
        if tag != version:
            info = (
                "Git tag '{0}' does not match the version of this package: {1}"
            ).format(tag, version)
            sys.exit(info)


setup(
    name="rsa-id-number",
    version=version,
    description="South African ID number utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teamgeek-io/rsa-id-number",
    author="Teamgeek",
    author_email="support@teamgeek.io",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="utilities, development",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
    cmdclass={"verify": VerifyVersionCommand},
)
