from setuptools import setup, find_packages

setup(
    name='speech_hints',
    version='1.0',
    packages=find_packages(),
    setup_requires=["wheel"],
    install_requires=[
    "Cython",
    "joblib",
    "pynini == 2.1.5",
    "regex",
    "tqdm"
    ],
)
