from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stock-market-tracker",
    version="1.0.0",
    author="Michal Uchwat",
    author_email="uchwatmichal@gmail.com",
    description="A stock market tracking system with AI predictions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "grpcio",
        "grpcio-tools",
        "requests",
        "kafka-python",
        "pymongo>=3.12",
        "tensorflow>=2.6",
        "numpy>=1.19",
        "pandas>=1.2",
        "scikit-learn>=0.24"
    ],
    entry_points={
        "console_scripts": [
            "run-api=api_gateway.api_gateway:create_app",
            "run-processor=stock_processor.stock_processor:serve",
            "run-fetcher=stock_fetcher.stock_fetcher:fetch_stock"
        ]
    },
    python_requires=">=3.7",
)
