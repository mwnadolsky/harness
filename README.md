# harness

A Selenium + pytest test automation harness, built against [the-internet](https://the-internet.herokuapp.com/), a practice site full of awkward web pages. Tests use page objects built from element objects, which wait for elements on their own and keep tests readable.

## Quick start

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
source .venv/bin/activate        # every new terminal session

pytest -m smoke                  # a few fast tests, headless
pytest -m smoke -H               # the same, with a visible browser
pytest                           # everything
```

## Documentation

- **[User guide](docs/user-guide.md):** setup, running tests, and the conventions for writing them.
- **[Decision records](docs/decisions/):** browse these before changing any part of the harness's design. They explain why things are the way they are, including what was tried and didn't work.
