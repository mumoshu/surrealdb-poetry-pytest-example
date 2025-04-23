This notes various issues the author encountered while building this project.

Hopefully this will be used by humas to fix similar issues, and AIs to learn not to generate code that does not work :)

ToC:

- [devcontainer](#devcontainer)
- [poetry](#poetry)
- [surrealdb.py](#surrealdb.py)

# devcontainer

## `[error] Following setting is deprecated: "python.linting.pylintEnabled"`

```
[error] All settings starting with "python.linting." are deprecated and can be removed from settings.
[error] Linting features have been moved to separate linter extensions.
[error] See here for more information: https://code.visualstudio.com/docs/python/linting
[error] Please install "pylint" extension: https://marketplace.visualstudio.com/items?itemName=ms-python.pylint
```

Resolution: Removed `customizations.vscode.settings["python.linting.pylintEnabled"]` from `devcontainer.json` and added `my-python.pylint` to `customizations.vscode.extensions`, ran `Rebuild Container`.

# poetry

## `The current project's supported Python range (>=3.8,<3.13) is not compatible with some of the required packages Python requirement:
  - aiohttp requires Python >=3.9, so it will not be installable for Python >=3.8,<3.9`

```
The current project's supported Python range (>=3.8,<3.13) is not compatible with some of the required packages Python requirement:
  - aiohttp requires Python >=3.9, so it will not be installable for Python >=3.8,<3.9

Because no versions of surrealdb match >1.0.3,<2.0.0
 and surrealdb (1.0.3) depends on aiohttp (3.11.11), surrealdb (>=1.0.3,<2.0.0) requires aiohttp (3.11.11).
So, because aiohttp (3.11.11) requires Python >=3.9
 and surrealdb-python-example depends on surrealdb (^1.0.3), version solving failed.

  * Check your dependencies Python requirement: The Python requirement can be specified via the `python` or `markers` properties

    For aiohttp, a possible solution would be to set the `python` property to ">=3.9,<3.13"
```

Resolution: Updated `pyproject.toml` like the below and ran `Rebuild Container`

```
[tool.poetry.dependencies]
python = ">=3.9,<3.13" # Compatible with Python 3.8 through 3.12
```

# surrealdb.py

## `There was a problem with the database: There was a problem with authentication` although the user/pass are correct

This could happen if you had named keyword arguments incorrectly:

For example, the below are incorrect:

```
db.signin({"user": DB_USER, "pass": DB_PASS})
```

It should be:

```
db.signin({"username": DB_USER, "password": DB_PASS})
```

# ms-python.pylint

## `Unable to import ` errors on almost all imports


# pytest

## `AttributeError: 'async_generator' object has no attribute '...'` on async fixtures

For me, this was due to an incorrect annotation on the async fixture.

Try `@pytest_asyncio.fixture(scope="function")` instead of `@pytest.fixture(scope="function")`.

```
# GOOD
@pytest_asyncio.fixture(scope="function")
async def db(request):
    # ...
    client = AsyncSurreal(url=DB_URL)
    yield client
    # ...

# BAD
@pytest.fixture(scope="function")
async def db(request):
    # ...
    client = AsyncSurreal(url=DB_URL)
    yield client
    # ...
```
