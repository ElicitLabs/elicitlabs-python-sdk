# Modal

Types:

```python
from elicitlabs.types import ModalLearnResponse, ModalQueryResponse, ModalQueryMultimodalityResponse
```

Methods:

- <code title="post /v1/modal/learn">client.modal.<a href="./src/elicitlabs/resources/modal.py">learn</a>(\*\*<a href="src/elicitlabs/types/modal_learn_params.py">params</a>) -> <a href="./src/elicitlabs/types/modal_learn_response.py">ModalLearnResponse</a></code>
- <code title="post /v1/modal/query">client.modal.<a href="./src/elicitlabs/resources/modal.py">query</a>(\*\*<a href="src/elicitlabs/types/modal_query_params.py">params</a>) -> <a href="./src/elicitlabs/types/modal_query_response.py">ModalQueryResponse</a></code>
- <code title="post /v1/modal/multimodal-query">client.modal.<a href="./src/elicitlabs/resources/modal.py">query_multimodality</a>(\*\*<a href="src/elicitlabs/types/modal_query_multimodality_params.py">params</a>) -> <a href="./src/elicitlabs/types/modal_query_multimodality_response.py">ModalQueryMultimodalityResponse</a></code>

# Users

Types:

```python
from elicitlabs.types import UserCreateOrGetResponse
```

Methods:

- <code title="post /v1/users">client.users.<a href="./src/elicitlabs/resources/users.py">create_or_get</a>(\*\*<a href="src/elicitlabs/types/user_create_or_get_params.py">params</a>) -> <a href="./src/elicitlabs/types/user_create_or_get_response.py">UserCreateOrGetResponse</a></code>

# Data

Types:

```python
from elicitlabs.types import DataIngestResponse
```

Methods:

- <code title="post /v1/data/ingest">client.data.<a href="./src/elicitlabs/resources/data/data.py">ingest</a>(\*\*<a href="src/elicitlabs/types/data_ingest_params.py">params</a>) -> <a href="./src/elicitlabs/types/data_ingest_response.py">DataIngestResponse</a></code>

## Job

Types:

```python
from elicitlabs.types.data import JobRetrieveStatusResponse
```

Methods:

- <code title="post /v1/data/job/status">client.data.job.<a href="./src/elicitlabs/resources/data/job.py">retrieve_status</a>(\*\*<a href="src/elicitlabs/types/data/job_retrieve_status_params.py">params</a>) -> <a href="./src/elicitlabs/types/data/job_retrieve_status_response.py">JobRetrieveStatusResponse</a></code>

# Health

Methods:

- <code title="get /health">client.health.<a href="./src/elicitlabs/resources/health.py">check</a>() -> object</code>

# Auth

## Keys

Types:

```python
from elicitlabs.types.auth import KeyCreateResponse, KeyListResponse, KeyRevokeResponse
```

Methods:

- <code title="post /v1/auth/keys">client.auth.keys.<a href="./src/elicitlabs/resources/auth/keys.py">create</a>(\*\*<a href="src/elicitlabs/types/auth/key_create_params.py">params</a>) -> <a href="./src/elicitlabs/types/auth/key_create_response.py">KeyCreateResponse</a></code>
- <code title="get /v1/auth/keys">client.auth.keys.<a href="./src/elicitlabs/resources/auth/keys.py">list</a>() -> <a href="./src/elicitlabs/types/auth/key_list_response.py">KeyListResponse</a></code>
- <code title="delete /v1/auth/keys/{api_key_id}">client.auth.keys.<a href="./src/elicitlabs/resources/auth/keys.py">revoke</a>(api_key_id) -> <a href="./src/elicitlabs/types/auth/key_revoke_response.py">KeyRevokeResponse</a></code>

# Personas

Types:

```python
from elicitlabs.types import PersonaCreateResponse, PersonaRetrieveResponse, PersonaListResponse
```

Methods:

- <code title="post /v1/personas">client.personas.<a href="./src/elicitlabs/resources/personas.py">create</a>(\*\*<a href="src/elicitlabs/types/persona_create_params.py">params</a>) -> <a href="./src/elicitlabs/types/persona_create_response.py">PersonaCreateResponse</a></code>
- <code title="get /v1/personas/{persona_id}">client.personas.<a href="./src/elicitlabs/resources/personas.py">retrieve</a>(persona_id) -> <a href="./src/elicitlabs/types/persona_retrieve_response.py">PersonaRetrieveResponse</a></code>
- <code title="get /v1/personas">client.personas.<a href="./src/elicitlabs/resources/personas.py">list</a>() -> <a href="./src/elicitlabs/types/persona_list_response.py">PersonaListResponse</a></code>

# Inference

Types:

```python
from elicitlabs.types import (
    InferenceGenerateCompletionResponse,
    InferenceGenerateMultimodalityCompletionResponse,
    InferenceGeneratePersonaChatResponse,
)
```

Methods:

- <code title="post /v1/inference/completion">client.inference.<a href="./src/elicitlabs/resources/inference.py">generate_completion</a>(\*\*<a href="src/elicitlabs/types/inference_generate_completion_params.py">params</a>) -> <a href="./src/elicitlabs/types/inference_generate_completion_response.py">InferenceGenerateCompletionResponse</a></code>
- <code title="post /v1/inference/multimodality-completion">client.inference.<a href="./src/elicitlabs/resources/inference.py">generate_multimodality_completion</a>(\*\*<a href="src/elicitlabs/types/inference_generate_multimodality_completion_params.py">params</a>) -> <a href="./src/elicitlabs/types/inference_generate_multimodality_completion_response.py">InferenceGenerateMultimodalityCompletionResponse</a></code>
- <code title="post /v1/inference/persona-chat">client.inference.<a href="./src/elicitlabs/resources/inference.py">generate_persona_chat</a>(\*\*<a href="src/elicitlabs/types/inference_generate_persona_chat_params.py">params</a>) -> <a href="./src/elicitlabs/types/inference_generate_persona_chat_response.py">InferenceGeneratePersonaChatResponse</a></code>

# Demo

Types:

```python
from elicitlabs.types import (
    DemoCreateUserResponse,
    DemoGenerateResetLinkResponse,
    DemoRequestPasswordResetResponse,
    DemoResetPasswordResponse,
    DemoRetrieveCurrentUserResponse,
    DemoSignInResponse,
    DemoSubmitEarlyAccessRequestResponse,
)
```

Methods:

- <code title="post /v1/demo/signup">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">create_user</a>(\*\*<a href="src/elicitlabs/types/demo_create_user_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo_create_user_response.py">DemoCreateUserResponse</a></code>
- <code title="post /v1/demo/get-reset-link">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">generate_reset_link</a>(\*\*<a href="src/elicitlabs/types/demo_generate_reset_link_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo_generate_reset_link_response.py">DemoGenerateResetLinkResponse</a></code>
- <code title="post /v1/demo/forgot-password">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">request_password_reset</a>(\*\*<a href="src/elicitlabs/types/demo_request_password_reset_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo_request_password_reset_response.py">DemoRequestPasswordResetResponse</a></code>
- <code title="post /v1/demo/reset-password">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">reset_password</a>(\*\*<a href="src/elicitlabs/types/demo_reset_password_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo_reset_password_response.py">DemoResetPasswordResponse</a></code>
- <code title="get /v1/demo/me">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">retrieve_current_user</a>() -> <a href="./src/elicitlabs/types/demo_retrieve_current_user_response.py">DemoRetrieveCurrentUserResponse</a></code>
- <code title="post /v1/demo/signin">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">sign_in</a>(\*\*<a href="src/elicitlabs/types/demo_sign_in_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo_sign_in_response.py">DemoSignInResponse</a></code>
- <code title="post /v1/demo/early-access">client.demo.<a href="./src/elicitlabs/resources/demo/demo.py">submit_early_access_request</a>(\*\*<a href="src/elicitlabs/types/demo_submit_early_access_request_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo_submit_early_access_request_response.py">DemoSubmitEarlyAccessRequestResponse</a></code>

## Auth

Types:

```python
from elicitlabs.types.demo import AuthAuthenticateWithGoogleResponse
```

Methods:

- <code title="post /v1/demo/auth/google">client.demo.auth.<a href="./src/elicitlabs/resources/demo/auth.py">authenticate_with_google</a>(\*\*<a href="src/elicitlabs/types/demo/auth_authenticate_with_google_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo/auth_authenticate_with_google_response.py">AuthAuthenticateWithGoogleResponse</a></code>

## Org

Types:

```python
from elicitlabs.types.demo import OrgListOrganizationMembersResponse
```

Methods:

- <code title="post /v1/demo/org/users">client.demo.org.<a href="./src/elicitlabs/resources/demo/org.py">list_organization_members</a>(\*\*<a href="src/elicitlabs/types/demo/org_list_organization_members_params.py">params</a>) -> <a href="./src/elicitlabs/types/demo/org_list_organization_members_response.py">OrgListOrganizationMembersResponse</a></code>
