# Inference

Types:

```python
from elicit_labs.types import InferenceProcessResponse
```

Methods:

- <code title="post /v1/inference">client.inference.<a href="./src/elicit_labs/resources/inference.py">process</a>(\*\*<a href="src/elicit_labs/types/inference_process_params.py">params</a>) -> <a href="./src/elicit_labs/types/inference_process_response.py">InferenceProcessResponse</a></code>

# Users

Types:

```python
from elicit_labs.types import UserCreateOrGetResponse
```

Methods:

- <code title="post /v1/users">client.users.<a href="./src/elicit_labs/resources/users.py">create_or_get</a>(\*\*<a href="src/elicit_labs/types/user_create_or_get_params.py">params</a>) -> <a href="./src/elicit_labs/types/user_create_or_get_response.py">UserCreateOrGetResponse</a></code>

# Data

Types:

```python
from elicit_labs.types import DataIngestResponse
```

Methods:

- <code title="post /v1/data/ingest">client.data.<a href="./src/elicit_labs/resources/data/data.py">ingest</a>(\*\*<a href="src/elicit_labs/types/data_ingest_params.py">params</a>) -> <a href="./src/elicit_labs/types/data_ingest_response.py">DataIngestResponse</a></code>

## Job

Types:

```python
from elicit_labs.types.data import JobRetrieveStatusResponse
```

Methods:

- <code title="post /v1/data/job/status">client.data.job.<a href="./src/elicit_labs/resources/data/job.py">retrieve_status</a>(\*\*<a href="src/elicit_labs/types/data/job_retrieve_status_params.py">params</a>) -> <a href="./src/elicit_labs/types/data/job_retrieve_status_response.py">JobRetrieveStatusResponse</a></code>

# Modal

Types:

```python
from elicit_labs.types import (
    AppContext,
    ModalAnalyzeTextResponse,
    ModalAnswerBackslashQueryResponse,
    ModalGenerateAutocompleteResponse,
    ModalInitializeResponse,
    ModalRespondToQueryResponse,
)
```

Methods:

- <code title="post /v1/modal/modal_reflection">client.modal.<a href="./src/elicit_labs/resources/modal.py">analyze_text</a>(\*\*<a href="src/elicit_labs/types/modal_analyze_text_params.py">params</a>) -> <a href="./src/elicit_labs/types/modal_analyze_text_response.py">ModalAnalyzeTextResponse</a></code>
- <code title="post /v1/modal/modal_backslash_q">client.modal.<a href="./src/elicit_labs/resources/modal.py">answer_backslash_query</a>(\*\*<a href="src/elicit_labs/types/modal_answer_backslash_query_params.py">params</a>) -> <a href="./src/elicit_labs/types/modal_answer_backslash_query_response.py">ModalAnswerBackslashQueryResponse</a></code>
- <code title="post /v1/modal/modal_autocomplete">client.modal.<a href="./src/elicit_labs/resources/modal.py">generate_autocomplete</a>(\*\*<a href="src/elicit_labs/types/modal_generate_autocomplete_params.py">params</a>) -> <a href="./src/elicit_labs/types/modal_generate_autocomplete_response.py">ModalGenerateAutocompleteResponse</a></code>
- <code title="post /v1/modal/modal_initialization">client.modal.<a href="./src/elicit_labs/resources/modal.py">initialize</a>(\*\*<a href="src/elicit_labs/types/modal_initialize_params.py">params</a>) -> <a href="./src/elicit_labs/types/modal_initialize_response.py">ModalInitializeResponse</a></code>
- <code title="post /v1/modal/modal_query">client.modal.<a href="./src/elicit_labs/resources/modal.py">respond_to_query</a>(\*\*<a href="src/elicit_labs/types/modal_respond_to_query_params.py">params</a>) -> <a href="./src/elicit_labs/types/modal_respond_to_query_response.py">ModalRespondToQueryResponse</a></code>

# Machine

Types:

```python
from elicit_labs.types import MachineLearnResponse, MachineQueryResponse
```

Methods:

- <code title="post /v1/machine/learn">client.machine.<a href="./src/elicit_labs/resources/machine.py">learn</a>(\*\*<a href="src/elicit_labs/types/machine_learn_params.py">params</a>) -> <a href="./src/elicit_labs/types/machine_learn_response.py">MachineLearnResponse</a></code>
- <code title="post /v1/machine/query">client.machine.<a href="./src/elicit_labs/resources/machine.py">query</a>(\*\*<a href="src/elicit_labs/types/machine_query_params.py">params</a>) -> <a href="./src/elicit_labs/types/machine_query_response.py">MachineQueryResponse</a></code>

# APIKeys

Types:

```python
from elicit_labs.types import APIKeyCreateResponse, APIKeyListResponse, APIKeyRevokeResponse
```

Methods:

- <code title="post /v1/api-keys/">client.api_keys.<a href="./src/elicit_labs/resources/api_keys.py">create</a>(\*\*<a href="src/elicit_labs/types/api_key_create_params.py">params</a>) -> <a href="./src/elicit_labs/types/api_key_create_response.py">APIKeyCreateResponse</a></code>
- <code title="get /v1/api-keys/">client.api_keys.<a href="./src/elicit_labs/resources/api_keys.py">list</a>() -> <a href="./src/elicit_labs/types/api_key_list_response.py">APIKeyListResponse</a></code>
- <code title="delete /v1/api-keys/{api_key_id}">client.api_keys.<a href="./src/elicit_labs/resources/api_keys.py">revoke</a>(api_key_id) -> <a href="./src/elicit_labs/types/api_key_revoke_response.py">APIKeyRevokeResponse</a></code>

# Health

Methods:

- <code title="get /health">client.health.<a href="./src/elicit_labs/resources/health.py">check</a>() -> object</code>
