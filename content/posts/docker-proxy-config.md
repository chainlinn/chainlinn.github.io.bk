---
title: "如何优雅的给 Docker 配置网络代理"
date: 2024-03-26T14:53:00+08:00
author: "CharyGao"
description: "Docker 的代理配置略显复杂，因为有三种场景（dockerd、容器运行、镜像构建）。本文梳理了每种场景的配置方式与适用条件。"
tags: ["Docker", "Proxy", "Network"]
categories: ["技术"]
draft: false
ShowToc: true
---

> 原文链接：https://www.cnblogs.com/Chary/p/18096678
> 作者：CharyGao（博客园 · 硅基文明）

有时因为网络原因，比如公司 NAT，需要使用代理。Docker 的代理配置略显复杂，因为有三种场景。但基本原理都是一致的，都是利用 Linux 的 `http_proxy` 等环境变量。

## Dockerd 代理

在执行 `docker pull` 时，是由守护进程 dockerd 来执行。因此，代理需要配在 dockerd 的环境中。而这个环境受 systemd 所管控，因此实际是 systemd 的配置。

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo touch /etc/systemd/system/docker.service.d/proxy.conf
```

在这个 `proxy.conf` 文件（可以是任意 `*.conf` 的形式）中，添加以下内容：

```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

其中 `proxy.example.com:8080` 要换成可用的免密代理。通常使用 cntlm 在本机自建免密代理，去对接公司的代理。

## Container 代理

在容器运行阶段，如果需要代理上网，则需要配置 `~/.docker/config.json`。以下配置只在 Docker 17.07 及以上版本生效。

```json
{
 "proxies":
 {
   "default":
   {
     "httpProxy": "http://proxy.example.com:8080",
     "httpsProxy": "http://proxy.example.com:8080",
     "noProxy": "localhost,127.0.0.1,.example.com"
   }
 }
}
```

这个是用户级的配置，除了 proxies，docker login 等相关信息也会在其中。而且还可以配置信息展示的格式、插件参数等。

此外，容器的网络代理也可以直接在其运行时通过 `-e` 注入 `http_proxy` 等环境变量。这两种方法分别适合不同场景：

- **config.json**：非常方便，默认在所有配置修改后启动的容器生效，适合个人开发环境。
- **-e 注入**：显式配置更好，适合 CI/CD 的自动构建环境或实际上线运行的环境，减轻对构建、部署环境的依赖。

## Docker Build 代理

虽然 `docker build` 的本质也是启动一个容器，但是环境会略有不同，用户级配置无效。在构建时，需要注入 `http_proxy` 等参数。

```bash
docker build . \
    --build-arg "HTTP_PROXY=http://proxy.example.com:8080/" \
    --build-arg "HTTPS_PROXY=http://proxy.example.com:8080/" \
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com" \
    -t your/image:tag
```

**注意**：无论是 `docker run` 还是 `docker build`，默认是网络隔绝的。如果代理使用的是 `localhost:3128` 这类，则会无效。这类仅限本地的代理，必须加上 `--network host` 才能正常使用。而一般则需要配置代理的外部 IP，而且代理本身要开启 Gateway 模式。

## 重启生效

代理配置完成后，reboot 重启当然可以生效，但不重启也行。

- **docker build 代理**：在执行前设置，修改后下次执行立即生效。
- **Container 代理**：修改后立即生效，但只针对以后启动的 Container，对已经启动的 Container 无效。
- **dockerd 代理**：实际上是改 systemd 的配置，需要重载 systemd 并重启 dockerd 才能生效。

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

检查确认环境变量已经正确配置：

```bash
sudo systemctl show --property=Environment docker
```

从 `docker info` 的结果中查看配置项：

```bash
docker info | grep Proxy
# 输出
#  HTTP Proxy: http://proxy.example.com:8080/
#  HTTPS Proxy: http://proxy.example.com:8080/
#  No Proxy: localhost,127.0.0.1,.example.com
```

## 补充：通过 daemon.json 配置代理

在 `/etc/docker/daemon.json` 中增加代理配置（此方式优先级高于 systemd 配置）：

```json
{
  "registry-mirrors": ["..."],
  "proxies": {
    "http-proxy": "http://proxy.example.com:8080",
    "https-proxy": "http://proxy.example.com:8080",
    "no-proxy": "registry.domain"
  }
}
```

重启 Docker 服务：

```bash
systemctl restart docker
```

## 总结

| 场景 | 配置方式 | 生效方式 |
|------|----------|----------|
| dockerd 拉取镜像 | systemd 或 daemon.json | `systemctl daemon-reload && systemctl restart docker` |
| 容器运行时 | `~/.docker/config.json` 或 `-e` 注入 | 自动生效 / 下次启动 |
| docker build | `--build-arg` 注入 | 立即生效 |
