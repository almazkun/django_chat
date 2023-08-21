# django_chat
- It is chat build with [django](https://pypi.org/project/Django/), [channels](https://pypi.org/project/channels/) and [daphne](https://pypi.org/project/daphne/).
- It has only one room.
- Open to every one to post a message.
- History is not saved.

# Demo
https://chat.akun.dev/

# Requirements
- Docker
- Make

# How to run
- `cp .env.example .env`
- `make build`
- `make run`
- `open http://localhost:8000`

# How to stop
- `make stop`

