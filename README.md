ivod-download-client
====================

Usage：
======

./ivod-downloader.py -l '2014-01-01'

-l 從該日期開始下載

-n 不下載圖片及影片，只抓資料


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
