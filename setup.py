
from setuptools import setup, find_packages

setup(
    name="perplexity-api",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.26.0",
        "perplexipy>=1.1.3"
    ],
)
