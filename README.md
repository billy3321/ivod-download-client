# ivod-download-client

安裝方式請參閱 [INSTALL.md](INSTALL.md)

## ivod\_single\_downloader.py

功能：下載單一段 VOD 檔案

用法：

```
ivod_single_downloader.py -u [影片播放網址]
```

範例：

```
ivod_single_downloader.py -u 'http://ivod.ly.gov.tw/Play/VOD/76394/300K'
```


## ivod\_downloader.py

設定檔：

```json
{
  "db": {
    "path": "ivod.db"
  },
  "download": {
    "path": "data"
  }
}
```

`ivod_downloader.py` 需要有設定檔在工作路徑（就是你執行下載指令的所在路徑）才能運算作，下面是檔案的範例。
檔名必需為 `config.json`


用法：

```
ivod_downloader.py -h
Usage: ivod_downloader.py [options]

Options:
  -h, --help            show this help message and exit
  -s START_DATE, --start-date=START_DATE
                        get video after date, format is %Y-%m-%d
  -e END_DATE, --end-date=END_DATE
                        get video before date, format is %Y-%m-%d
  -c COMIT_CODE, --committee=COMIT_CODE
                        parse committee, please input code.
  -n, --no-download     don't download resource
  -l LIMIT_SPEED, --limit-speed=LIMIT_SPEED
                        download speed, unit is kb/s
```

範例（指定時間）：

```
ivod_downloader.py -s '2014-01-01'
```

```
ivod_downloader.py -s '2014-01-01' -e '2014-10-01'
```

範例（指定委員會）：

```
ivod_downloader.py -c 8
```

```
ivod_downloader.py -c 8 -s '2014-09-01'
```

範例（僅抓資料）：

```
ivod_downloader.py -n
```

```
ivod_downloader.py -n -c 8 -s '2014-09-01'
```


## run\_daily.py

(維修中)


# 檔案與描述資料說明

抓到的資料會放在 ivod.db，是 sqlite3 的 Database。

抓下來的檔案會放在data資料夾中，目錄結構為：

data/屆/會期/委員會代碼/日期

檔案命名方式：

完整檔案：

日期-委員會代碼。

委員發言片斷：

日期-委員會代碼-順序-委員名。


相依性：
======

Python：Beautifulsoap, youtube_dl

