# Modal

Types:

```python
from elicitlabs.types import ModalLearnResponse, ModalQueryResponse
```

Methods:

- <code title="post /v1/modal/learn">client.modal.<a href="./src/elicitlabs/resources/modal.py">learn</a>(\*\*<a href="src/elicitlabs/types/modal_learn_params.py">params</a>) -> <a href="./src/elicitlabs/types/modal_learn_response.py">ModalLearnResponse</a></code>
- <code title="post /v1/modal/query">client.modal.<a href="./src/elicitlabs/resources/modal.py">query</a>(\*\*<a href="src/elicitlabs/types/modal_query_params.py">params</a>) -> <a href="./src/elicitlabs/types/modal_query_response.py">ModalQueryResponse</a></code>

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

# Projects

Types:

```python
from elicitlabs.types import (
    ProjectCreateResponse,
    ProjectRetrieveResponse,
    ProjectListResponse,
    ProjectDeleteResponse,
)
```

Methods:

- <code title="post /v1/projects">client.projects.<a href="./src/elicitlabs/resources/projects.py">create</a>(\*\*<a href="src/elicitlabs/types/project_create_params.py">params</a>) -> <a href="./src/elicitlabs/types/project_create_response.py">ProjectCreateResponse</a></code>
- <code title="get /v1/projects/{project_id}">client.projects.<a href="./src/elicitlabs/resources/projects.py">retrieve</a>(project_id) -> <a href="./src/elicitlabs/types/project_retrieve_response.py">ProjectRetrieveResponse</a></code>
- <code title="get /v1/projects">client.projects.<a href="./src/elicitlabs/resources/projects.py">list</a>() -> <a href="./src/elicitlabs/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /v1/projects/{project_id}">client.projects.<a href="./src/elicitlabs/resources/projects.py">delete</a>(project_id) -> <a href="./src/elicitlabs/types/project_delete_response.py">ProjectDeleteResponse</a></code>

# Chat

Types:

```python
from elicitlabs.types import ChatCreateCompletionResponse
```

Methods:

- <code title="post /v1/chat/completions">client.chat.<a href="./src/elicitlabs/resources/chat.py">create_completion</a>(\*\*<a href="src/elicitlabs/types/chat_create_completion_params.py">params</a>) -> <a href="./src/elicitlabs/types/chat_create_completion_response.py">ChatCreateCompletionResponse</a></code>

# Text

Types:

```python
from elicitlabs.types import TextGenerateResponse
```

Methods:

- <code title="post /v1/text/generations">client.text.<a href="./src/elicitlabs/resources/text.py">generate</a>(\*\*<a href="src/elicitlabs/types/text_generate_params.py">params</a>) -> <a href="./src/elicitlabs/types/text_generate_response.py">TextGenerateResponse</a></code>

# Images

Types:

```python
from elicitlabs.types import ImageGenerateResponse
```

Methods:

- <code title="post /v1/images/generations">client.images.<a href="./src/elicitlabs/resources/images.py">generate</a>(\*\*<a href="src/elicitlabs/types/image_generate_params.py">params</a>) -> <a href="./src/elicitlabs/types/image_generate_response.py">ImageGenerateResponse</a></code>

# Audio

Types:

```python
from elicitlabs.types import AudioGenerateResponse
```

Methods:

- <code title="post /v1/audio/generations">client.audio.<a href="./src/elicitlabs/resources/audio.py">generate</a>(\*\*<a href="src/elicitlabs/types/audio_generate_params.py">params</a>) -> <a href="./src/elicitlabs/types/audio_generate_response.py">AudioGenerateResponse</a></code>

# Video

Types:

```python
from elicitlabs.types import VideoGenerateResponse
```

Methods:

- <code title="post /v1/video/generations">client.video.<a href="./src/elicitlabs/resources/video.py">generate</a>(\*\*<a href="src/elicitlabs/types/video_generate_params.py">params</a>) -> <a href="./src/elicitlabs/types/video_generate_response.py">VideoGenerateResponse</a></code>
