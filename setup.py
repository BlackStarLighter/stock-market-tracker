from setuptools import setup, find_packages

setup(
    name="stock-market-tracker",
    version="1.0.0",
    author="Michal Uchwat",
    author_email="uchwatmichal@gmail.com",
    description="A stock market tracking system with AI predictions.",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "grpcio",
        "grpcio-tools",
        "requests",
        "kafka-python",
        "pymongo",
        "tensorflow",
        "numpy",
        "pandas",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "run-api=api_gateway.api_gateway:app",
            "run-processor=stock_processor.stock_processor:serve",
            "run-fetcher=stock_fetcher.stock_fetcher:fetch_stock"
        ]
    },
    python_requires=">=3.7",
)
