## インストール

1. `git clone`

```
git clone https://github.com/hamadatakaki/kurage-util-scripts.git .kurage-util-scripts
```

2. `PATH` を設定

`.bashrc` などに以下を追記する

```
export PATH="$HOME/.kurage-util-scripts/bin/:$PATH"
```

3. `.env` を設定

```
cd ~/.kurage-util-scripts
cat .env.example > .env
vim .env
```

4. 依存関係のセットアップ

```
cd ~/.kurage-util-scripts
tools/setup.sh
```

5. `kusdoctor` を叩いてテスト

## 新しいスクリプトの追加

1. `src/` の直下に実行用の Python ファイルを追加
2. `bin/` にシンボリックリンクを作成

```
cd bin/
ln -s ../src/{script}.py {command}
cd ..
```

3. 実行権限を設定

```
chmod +x bin/{command}
```
