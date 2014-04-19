ivod-download-client
====================

Usage：
======

首先先複製設定檔

cp config.json.default config.json

接著執行主程式

./ivod-downloader.py -s '2014-01-01'

-s 從該日期開始下載

-e 下載到該日期

-n 不下載圖片及影片，只抓資料

-l 速度限制，單位為kb/s

如果很懶，可以直接執行run_daily.py，會自動抓從今天起前5天的影片。

./run_daily.py


抓到的資料會放在 ivod.db，是sqlite3格式的Database

抓下來的檔案會放在data資料夾中，目錄結構為：

data/屆/會期/委員會代碼/日期

檔案命名方式：

完整檔案：

日期-委員會代碼。

委員發言片斷：

日期-委員會代碼-順序-委員名。


相依性：
======

Python：Beautifulsoap

PHP：curl

特別聲明：
======
AdobeHDS.php is come from https://github.com/K-S-V/Scripts
