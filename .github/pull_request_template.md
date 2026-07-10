## Summary

Describe the problem, the engineering change, and the expected outcome.

## Change type

- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Test
- [ ] Documentation
- [ ] Security
- [ ] Dependency / supply chain
- [ ] Deployment / release

## Validation evidence

- [ ] Python syntax validation passes.
- [ ] Ruff correctness checks pass.
- [ ] Domain and API tests pass.
- [ ] Coverage and JUnit evidence are generated.
- [ ] Streamlit smoke testing passes when applicable.
- [ ] API container builds and its health endpoint passes.

Commands or evidence:

```text
Paste concise validation evidence here.
```

## Responsible-use and data-safety review

- [ ] No real patient data, PHI, credentials, or private model artifacts are included.
- [ ] The change does not present heuristic output as a diagnosis or calibrated probability.
- [ ] Non-clinical disclaimers remain accurate and visible.
- [ ] Any new data source has documented provenance, license, and de-identification status.
- [ ] Any new trained model documents intended use, limitations, validation, and versioning.

## API and compatibility impact

Describe request/response changes, migration needs, and backward compatibility.

## Security and supply-chain impact

Describe input-boundary, dependency, secret, container, privacy, or vulnerability implications.

## Deployment impact

Describe Streamlit, Docker, GitHub Actions, GHCR, configuration, and runtime effects.

## Rollback plan

Explain how to restore the previous behavior safely.

## Documentation

- [ ] README updated.
- [ ] CHANGELOG updated.
- [ ] Deployment or operating runbooks updated.
- [ ] No documentation change required.
