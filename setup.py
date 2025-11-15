"""
Setup script for AI Model installation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-orchestrator-model",
    version="1.0.0",
    author="AI Development Team",
    description="Advanced AI Model with multi-capability support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-model",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "aiohttp>=3.9.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "speech-recognition>=3.10.0",
        "gtts>=2.4.0",
        "python-pptx>=0.6.21",
        "reportlab>=4.0.0",
        "numpy>=1.24.0",
        "pandas>=2.1.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.8.0",
        "plotly>=5.18.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-model=core.orchestrator:main",
        ],
    },
)