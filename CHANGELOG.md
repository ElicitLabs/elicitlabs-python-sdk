# Changelog

## 0.9.0 (2026-01-26)

Full Changelog: [v0.8.0...v0.9.0](https://github.com/ElicitLabs/elicitlabs-python-sdk/compare/v0.8.0...v0.9.0)

### Features

* **api:** api update ([b14e4b0](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/b14e4b01337ebdbc656bcd405b60eab9267aebb3))
* **api:** api update ([aa93942](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/aa93942ad5991de2a5fccc42fb7d26ad6ecf84ea))


### Chores

* **ci:** upgrade `actions/github-script` ([3d9756c](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/3d9756c3ab8c348f1dbbaca897d4c1220a9a7b93))

## 0.8.0 (2026-01-21)

Full Changelog: [v0.7.0...v0.8.0](https://github.com/ElicitLabs/elicitlabs-python-sdk/compare/v0.7.0...v0.8.0)

### Features

* **api:** api update ([0996f7d](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/0996f7d53826b0c8e7ba4669e98f7440a93e337f))
* **api:** manual updates ([d312abd](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/d312abde58f65b07278901c9cf734eb06a711e39))
* **client:** add support for binary request streaming ([2341d22](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/2341d229279f4daa846b64d6903d2c266f980675))


### Bug Fixes

* use async_to_httpx_files in patch method ([d336a2e](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/d336a2e3294f69af761adb7b0b23215aa49d51de))


### Chores

* **internal:** add `--fix` argument to lint script ([4f1c89a](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/4f1c89aaabcbbc08ec568fe33e989f0049ebe755))
* **internal:** add missing files argument to base client ([26a0750](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/26a0750857142de33ab48c5c33d0f0cfc61d006f))
* **internal:** codegen related update ([b67a89e](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/b67a89ef631a9803775da8826cd15ede8e044d1f))
* **internal:** update `actions/checkout` version ([777d999](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/777d9998a8b53b31034f1828bd560051fe01490f))
* speedup initial import ([1554754](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/15547548a598a3c5cbdfa8f16edc98275661afc4))

## 0.7.0 (2025-12-10)

Full Changelog: [v0.6.0...v0.7.0](https://github.com/ElicitLabs/elicitlabs-python-sdk/compare/v0.6.0...v0.7.0)

### Features

* **api:** api update ([70750c2](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/70750c2e41b5f0573ef864b70c74ba369aa07a4e))


### Bug Fixes

* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([afbb39d](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/afbb39dea42c974c8e4b94d69d773a5feb2e30c9))


### Chores

* add missing docstrings ([5f030dd](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/5f030ddb86bf5ebda28d31716002a20a645c4a09))
* **docs:** use environment variables for authentication in code snippets ([3826b97](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/3826b970f56bb2300346d1e1807dd2a19760f91e))
* update lockfile ([675b015](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/675b015b3eec8f12d99699f2b7b5b9e3f72effbf))

## 0.6.0 (2025-12-02)

Full Changelog: [v0.5.0...v0.6.0](https://github.com/ElicitLabs/elicitlabs-python-sdk/compare/v0.5.0...v0.6.0)

### Features

* **api:** manual updates ([f8c968a](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/f8c968a1fd82c219debc9c537f21be860cc8f7fb))


### Bug Fixes

* ensure streams are always closed ([60ac39d](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/60ac39df028f9f4b0ee180c4faeb017392557c88))


### Chores

* add Python 3.14 classifier and testing ([628acbc](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/628acbcfa9cd4532dcab07a46d2a006da65f85ab))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([5c56d92](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/5c56d92cd03f9d2cc935d0118405d04d9bf5bb0a))

## 0.5.0 (2025-11-17)

Full Changelog: [v0.4.0...v0.5.0](https://github.com/ElicitLabs/elicitlabs-python-sdk/compare/v0.4.0...v0.5.0)

### Features

* **api:** api update ([b1fcbd8](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/b1fcbd823d9bf5000c0626c598830a23ab2bcb7a))
* **api:** api update ([6a8b0d0](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/6a8b0d042c95360a1d871a3ad2fb5e4ec6b1295a))
* **api:** manual updates ([9db0c86](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/9db0c86a3ec44f6fb349f4502ae376b97d65968d))


### Bug Fixes

* compat with Python 3.14 ([808f6b0](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/808f6b07bbe32ffc705a5419c17c7862de67799f))
* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([b8eee50](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/b8eee509abf2bb51c2f3b37af1f6cd2f789247a7))


### Chores

* **package:** drop Python 3.8 support ([faaa46f](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/faaa46fd3cea5183eed63b484b276649b461c382))

## 0.4.0 (2025-11-05)

Full Changelog: [v0.3.0...v0.4.0](https://github.com/ElicitLabs/elicitlabs-python-sdk/compare/v0.3.0...v0.4.0)

### Features

* **api:** manual updates ([0818987](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/0818987037d4e3386070e610340acd320081fc91))


### Chores

* update SDK settings ([70d0789](https://github.com/ElicitLabs/elicitlabs-python-sdk/commit/70d07899aa34ad2e85281141bb9e732365be7571))

## 0.3.0 (2025-11-05)

Full Changelog: [v0.2.0...v0.3.0](https://github.com/ElicitLabs/modal-python-sdk/compare/v0.2.0...v0.3.0)

### Features

* **api:** api update ([8bd3668](https://github.com/ElicitLabs/modal-python-sdk/commit/8bd366885e229a8c5d441cde63d8c3a619314d93))
* **api:** api update ([f29b786](https://github.com/ElicitLabs/modal-python-sdk/commit/f29b78675d71ee2dac399cd3f4d82d9dff051852))
* **api:** manual updates ([ba6ef0a](https://github.com/ElicitLabs/modal-python-sdk/commit/ba6ef0a31e3813ebb4e8b6fe225454feaee3547e))


### Bug Fixes

* **client:** close streams without requiring full consumption ([27a0353](https://github.com/ElicitLabs/modal-python-sdk/commit/27a03536d288096908e367425972b75644efb436))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([afa3e51](https://github.com/ElicitLabs/modal-python-sdk/commit/afa3e51305524e93d3360ddaafde1441a8bdf308))
* do not install brew dependencies in ./scripts/bootstrap by default ([e6ffca9](https://github.com/ElicitLabs/modal-python-sdk/commit/e6ffca92643caf732e6beb205a9b713f21ae7dfd))
* **internal/tests:** avoid race condition with implicit client cleanup ([1967ee1](https://github.com/ElicitLabs/modal-python-sdk/commit/1967ee1c2e31d221f21b2088b37978e0198b9881))
* **internal:** codegen related update ([b3f7c70](https://github.com/ElicitLabs/modal-python-sdk/commit/b3f7c70f00076fb991fc1420a7de54f6d8c5281b))
* **internal:** detect missing future annotations with ruff ([03e4e51](https://github.com/ElicitLabs/modal-python-sdk/commit/03e4e5109d7cba6b2b16b15a75f24d2de6cf1690))
* **internal:** grammar fix (it's -&gt; its) ([8167d88](https://github.com/ElicitLabs/modal-python-sdk/commit/8167d88a50a836585ac5ce2568d1080f90dc35ef))
* **internal:** update pydantic dependency ([e27bd49](https://github.com/ElicitLabs/modal-python-sdk/commit/e27bd490de9263f1a5121ed5011bc9b504056376))
* **types:** change optional parameter type from NotGiven to Omit ([ece45db](https://github.com/ElicitLabs/modal-python-sdk/commit/ece45db796e756a686544330335fbe7965c8fa0f))

## 0.2.0 (2025-09-06)

Full Changelog: [v0.1.0...v0.2.0](https://github.com/ElicitLabs/modal-python-sdk/compare/v0.1.0...v0.2.0)

### Features

* **api:** api update ([29ef4d5](https://github.com/ElicitLabs/modal-python-sdk/commit/29ef4d55e71b8c6bcb31d99136241d3cc531f2f6))
* **api:** manual updates ([b25a157](https://github.com/ElicitLabs/modal-python-sdk/commit/b25a157233997452f3c82dbd6b16492e8b9894dd))
* improve future compat with pydantic v3 ([b278a4f](https://github.com/ElicitLabs/modal-python-sdk/commit/b278a4faf1edbfd3637955d45312e6fa6320faa7))


### Chores

* **internal:** move mypy configurations to `pyproject.toml` file ([3863623](https://github.com/ElicitLabs/modal-python-sdk/commit/3863623680a802829f8f8f6d2282fea29c3f7ac7))

## 0.1.0 (2025-09-03)

Full Changelog: [v0.0.1...v0.1.0](https://github.com/ElicitLabs/modal-python-sdk/compare/v0.0.1...v0.1.0)

### Features

* **api:** update via SDK Studio ([373dbce](https://github.com/ElicitLabs/modal-python-sdk/commit/373dbceed8aa5cde59951b759c737f31c34ab81c))
* **api:** update via SDK Studio ([2178bdf](https://github.com/ElicitLabs/modal-python-sdk/commit/2178bdff85ce23510c4fbaf1bb1475eeae293d0d))


### Chores

* update SDK settings ([0e0d556](https://github.com/ElicitLabs/modal-python-sdk/commit/0e0d556f761aa830ed1008eafe5789dafc5dab80))
* update SDK settings ([36952f0](https://github.com/ElicitLabs/modal-python-sdk/commit/36952f0edb8bda863589bb4c126d1217d36a91d1))
