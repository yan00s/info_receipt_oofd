# info_receipt_oofd
Installation:
    git-clone https://github.com/yan00s/info_receipt_oofd
    cd *path to dir*
    pip install -r requirements.txt
    put token api tg bot with key "api_tg_qr" to .env

    maybe you need additional intall packets (you can find packets in file "maybe_need.txt")


Setup service:
    move receiptqr.service in /etc/systemd/system

    you need edit it a bit and change the path / version python

    enable receiptqr.service
    start receiptqr.service
