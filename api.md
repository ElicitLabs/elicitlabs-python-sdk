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
from elicitlabs.types import DataConfirmUploadResponse, DataGetUploadURLResponse, DataIngestResponse
```

Methods:

- <code title="post /v1/data/ingest/confirm-upload">client.data.<a href="./src/elicitlabs/resources/data/data.py">confirm_upload</a>(\*\*<a href="src/elicitlabs/types/data_confirm_upload_params.py">params</a>) -> <a href="./src/elicitlabs/types/data_confirm_upload_response.py">DataConfirmUploadResponse</a></code>
- <code title="post /v1/data/ingest/upload-url">client.data.<a href="./src/elicitlabs/resources/data/data.py">get_upload_url</a>(\*\*<a href="src/elicitlabs/types/data_get_upload_url_params.py">params</a>) -> <a href="./src/elicitlabs/types/data_get_upload_url_response.py">DataGetUploadURLResponse</a></code>
- <code title="post /v1/data/ingest">client.data.<a href="./src/elicitlabs/resources/data/data.py">ingest</a>(\*\*<a href="src/elicitlabs/types/data_ingest_params.py">params</a>) -> <a href="./src/elicitlabs/types/data_ingest_response.py">DataIngestResponse</a></code>

## Job

Types:

```python
from elicitlabs.types.data import JobCancelResponse
```

Methods:

- <code title="post /v1/data/job/cancel">client.data.job.<a href="./src/elicitlabs/resources/data/job.py">cancel</a>(\*\*<a href="src/elicitlabs/types/data/job_cancel_params.py">params</a>) -> <a href="./src/elicitlabs/types/data/job_cancel_response.py">JobCancelResponse</a></code>

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

# Projects

Types:

```python
from elicitlabs.types import (
    ProjectCreateResponse,
    ProjectRetrieveResponse,
    ProjectListResponse,
    ProjectDeleteResponse,
    ProjectCloneResponse,
)
```

Methods:

- <code title="post /v1/projects">client.projects.<a href="./src/elicitlabs/resources/projects.py">create</a>(\*\*<a href="src/elicitlabs/types/project_create_params.py">params</a>) -> <a href="./src/elicitlabs/types/project_create_response.py">ProjectCreateResponse</a></code>
- <code title="get /v1/projects/{project_id}">client.projects.<a href="./src/elicitlabs/resources/projects.py">retrieve</a>(project_id, \*\*<a href="src/elicitlabs/types/project_retrieve_params.py">params</a>) -> <a href="./src/elicitlabs/types/project_retrieve_response.py">ProjectRetrieveResponse</a></code>
- <code title="get /v1/projects">client.projects.<a href="./src/elicitlabs/resources/projects.py">list</a>(\*\*<a href="src/elicitlabs/types/project_list_params.py">params</a>) -> <a href="./src/elicitlabs/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /v1/projects/{project_id}">client.projects.<a href="./src/elicitlabs/resources/projects.py">delete</a>(project_id, \*\*<a href="src/elicitlabs/types/project_delete_params.py">params</a>) -> <a href="./src/elicitlabs/types/project_delete_response.py">ProjectDeleteResponse</a></code>
- <code title="post /v1/projects/clone">client.projects.<a href="./src/elicitlabs/resources/projects.py">clone</a>(\*\*<a href="src/elicitlabs/types/project_clone_params.py">params</a>) -> <a href="./src/elicitlabs/types/project_clone_response.py">ProjectCloneResponse</a></code>

# Images

Types:

```python
from elicitlabs.types import ImageGenerateResponse
```

Methods:

- <code title="post /v1/images/generations">client.images.<a href="./src/elicitlabs/resources/images.py">generate</a>(\*\*<a href="src/elicitlabs/types/image_generate_params.py">params</a>) -> <a href="./src/elicitlabs/types/image_generate_response.py">ImageGenerateResponse</a></code>
