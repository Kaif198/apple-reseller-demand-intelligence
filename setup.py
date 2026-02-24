from setuptools import setup, find_packages

setup(
    name="apple-demand-planner",
    version="1.0.0",
    author="Mohammed Kaif Ahmed",
    description="Apple Reseller Channel Demand Planning & Inventory Intelligence Platform",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
)
