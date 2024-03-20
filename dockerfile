FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    # インストールしたパッケージのダウロードファイルを削除
    && apt-get clean \ 
    # パッケージのリスト(ログファイル)を削除
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python -

# Poetryのパスの設定
ENV PATH /root/.local/bin:$PATH

# Poetryが仮想環境を生成しないようにする
RUN poetry config virtualenvs.create false

COPY ["./pyproject.toml", "./poetry.lock", "/app/"]
RUN poetry install