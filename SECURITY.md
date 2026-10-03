# Security policy

binomcikit is a numerical library: it reads no files or network input of its own, and its public functions take numbers and arrays. The
realistic security concerns are limited (for example, a crafted argument that makes a function run for an unbounded time or use
unbounded memory, or a problem in the build and release pipeline).

## Supported versions

Only the latest released version receives fixes. The project is pre-1.0 in practice (PyPI still carries an old 0.0.5), so there is no
long-term-support branch.

## Reporting a vulnerability

Please report it privately through GitHub: on the repository page open **Security → Report a vulnerability**
(<https://github.com/pranava-ba/binomcikit/security/advisories/new>), and do not open a public issue for it. Include the call or input that
triggers it, the versions involved and what you expected.

You should get an acknowledgement within a week. Fixes for confirmed issues are released as soon as they are ready and credited in
`CHANGELOG.md` unless you prefer otherwise.

> Maintainer note: GitHub's private vulnerability reporting must be switched on in the repository settings
> (Settings → Code security) for the link above to work.
