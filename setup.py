from setuptools import setup, find_packages

setup(
    name="gfg",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pymongo",
        "python-jose",
        "bcrypt==4.1.2",
        "python-dotenv>=0.19.0",
        "slowapi==0.1.8",
    ],
)
