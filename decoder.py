from enum import IntEnum

# 列挙型の定義
class MessageType(IntEnum):
  SENDFILE = 0x02,# ファイル送信コマンド
  SENDFILEEND = 0x03,# ファイル送信終了コマンド