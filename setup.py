from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="career-scout-telegram",
    version="0.1.0",
    description="Telegram job vacancy parser with keyword filtering",
    author="Mikhail Tabakaev",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'career-scout=src.parser:main',
            'career-scout-logs=src.commands.watch_logs:watch_logs',
            'career-scout-clear-cache=src.commands.clear_cache:clear_cache',
        ],
    }
) 