# Release process

1. Run the README checks, build docs, and inspect the endpoint manifest diff.
2. Install the built wheel and sdist separately into clean environments; verify imports and model aliases. Run optional live smoke tests with an IP-allowlisted `CLASH_ROYALE_API_TOKEN`.
3. Push changes, wait for the CI matrix, and tag `v<version>` matching pyproject.toml and __version__. Create a GitHub release with the wheel and sdist.
4. The release workflow builds and validates distributions, then publishes through the `pypi` environment using Trusted Publishing. Enable the repository variable `PYPI_TRUSTED_PUBLISHING=true` after configuring the binding. Configure PyPI with owner EchterAlsFake, repository ClashRoyaleAPI, workflow release.yml, environment pypi. A one-time local token publication can be used instead; do not put the token in the repository.
5. Build the server-compatible content fragment with `uv run python scripts/build_docs.py`. Copy docs/clashroyaleapi.html to Server/docs/content/clashroyaleapi.html. Stage the existing server documentation builder and validate its output before installation, because it clears docs/dist.
6. Verify https://pypi.org/project/ClashRoyaleAPI/, clean pip installation, GitHub release assets, and https://docs.echteralsfake.me/clashroyaleapi/.

The server deployment helper belongs to the separate Server project. Deploy only the documentation files for this release; do not deploy unrelated server modifications. CI does not hold server SSH credentials.
