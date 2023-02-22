# info_receipt_oofd
Installation:
  1. git-clone https://github.com/yan00s/info_receipt_oofd
  2. cd *path to dir*
  3. pip install -r requirements.txt
  4. put token api tg bot with key "api_tg_qr" to .env
        
maybe you also need additional intall packets (you can find packets in file "maybe_need.txt")

you need edit "receiptqr.service" a bit and change the path / version python
Setup service:
  1. move receiptqr.service in /etc/systemd/system
  2. enable receiptqr.service
  3. start receiptqr.service
