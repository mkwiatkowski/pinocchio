from setuptools import setup

setup(
    name='pinocchio',
    version="0.4.3",
    description = 'pinocchio plugins for the nose testing framework',
    author = 'C. Titus Brown and Michal Kwiatkowski',
    author_email = 'titus@idyll.org,michal@trivas.pl',
    license = 'MIT',

    url = 'https://github.com/mkwiatkowski/pinocchio',

    long_description = """\
Extra plugins for the nose testing framework.  Provides tools for flexibly
assigning decorator tags to tests, choosing tests based on their
runtime, doing moderately sophisticated code coverage analysis
of your unit tests, and making your test descriptions look like
specifications.
""",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Plugins",
        "Topic :: Software Development :: Testing"
    ],

    packages = ['pinocchio'],
    entry_points = {
        'nose.plugins': [
            'figleaf-sections = pinocchio.figleaf_sections:FigleafSections',
            ],
        'nose.plugins.0.10': [
            'decorator = pinocchio.decorator:Decorator',
            'output-save = pinocchio.output_save:OutputSave',
            'spec = pinocchio.spec:Spec',
            'stopwatch = pinocchio.stopwatch:Stopwatch',
        ]},
    install_requires = ['colorama'],
)
