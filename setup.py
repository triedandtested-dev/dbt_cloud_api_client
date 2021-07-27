import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbt-cloud-api-client",
    version="0.0.1",
    author="Tried and Tested",
    author_email="bryan@triedandtested.dev",
    description="DBT Cloud API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/triedandtested-dev/dbt_cloud_api_client",
    project_urls={
        "Bug Tracker": "https://github.com/triedandtested-dev/dbt_cloud_api_client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
