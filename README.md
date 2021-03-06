# poetry-fastapi-practice

## Install pyenv
- bash
  - git clone git://github.com/yyuu/pyenv.git ~/.pyenv
  - write the pyenv path on `.bash_profile`

```.bash_profile
+ export PATH="$HOME/.pyenv/bin:$PATH"
+ eval "$(pyenv init --path)"
```

## Install python

```bash
$ pyenv install --list # The list of python version can install
$ pyenv install 3.x.x
$ pyenv global 3.x.x
```

## Install poetry

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```

- Add poetry PATH on `.bash_profile`

```
+ export PATH="$HOME/.poetry/bin:$PATH"
```

- Change python path handled by poetry to pyenv

```
$ poetry env use {pyenv path}
```

## start project

```
git clone git@github.com:daitasu/fastapi-poetry-practice.git

## boot db
docker-compose up

## boot app on dev
poetry run uvicorn app.api.server:app --reload
```
