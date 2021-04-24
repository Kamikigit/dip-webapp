# dip-webapp

## Login
```
$ az login
$ az acr login --name dipweb # レジストリにアクセスできるようにする
$ az acr credential show --resource-group AppSvc-DockerTutorial-rg --name myResourceGroup

...
ログインに必要な情報が出力される
...

$ docker login dipweb.azurecr.io --username dipweb

# 前のコマンドで得られたパスワードでログイン
```

## Build

```
docker-compose build
docker-compose push
```

## Run
```
docker-compose up -d
```
