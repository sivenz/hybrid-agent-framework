"""
Hybrid Agent Framework - OpenAI + Claude Power Duo
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hybrid-agent-framework",
    version="0.1.0",
    author="Moses Rajan",
    author_email="moses@cogniolab.com",
    description="Combine OpenAI's orchestration with Claude's system execution for production-ready AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mosesrajan/hybrid-agent-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "openai-agents>=0.1.0",
        "anthropic>=0.18.0",
        "pydantic>=2.0.0",
        "aiohttp>=3.9.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ],
        "tracing": [
            "logfire>=0.1.0",
            "opentelemetry-api>=1.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hybrid-agent=hybrid_agents.cli:main",
        ],
    },
)
