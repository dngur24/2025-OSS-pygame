# 2025-OSS
2024 OSS 과제물을 바탕으로 일부 수정

[VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/)

```bash
xhost +
```

```bash
docker build -t [pygame-alpha]
```

```bash
docker run -it --env="DISPLAY=[default switch(vLan)172.20.80.1]:0" -v /tmp/.X11-unix:/tmp/.X11-unix [이미지pygame-alpha] bash
```
