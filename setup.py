from os import path

from setuptools import find_packages, setup

__version__ = "0.3.1"


# Read long description from README.md
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()


setup(
    name="flipgenic",
    version=__version__,
    description="High-speed conversational dialogue engine for chatbots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Thwaites",
    author_email="danthwaites30@btinternet.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="conversation dialogue engine chat chatbot",
    url="https://github.com/AlphaMycelium/flipgenic",
    project_urls={
        "Bug Reports": "https://github.com/AlphaMycelium/flipgenic/issues",
        "Source": "https://github.com/AlphaMycelium/flipgenic",
    },
    packages=find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.6,<4",
    install_requires=[
        "sqlalchemy >=1.3,<4",
        "ngt >=1,<2",
        "spacy >=2,<3",
        "mathparse <1",
    ],
)
