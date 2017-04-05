# pytg_sctipt
scripts of python telegram-cli by chliny

## 依赖
- [telegram_cli](https://github.com/vysheng/tg)
- [pytg](https://github.com/luckydonald/pytg)
- [proxychains-ng](https://github.com/rofl0r/proxychains-ng)
- Python3

## 用法
- `pythn3 met.py [groupname|username]`  自动met个人/群里所有成员

    - 第一次使用telegram-cli需要手动启动并配置登录手机号.


- `pythn3 replymet.py [ingress_id] [groupname1] [groupname2] ... & `  自动回met

    - 同上，第一次使用telegram-cli㙘手动启动

    - groupname 为要监听的群，多个群以空格分开。不加此参数时监听所有群

