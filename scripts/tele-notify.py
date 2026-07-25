#!/usr/bin/env python3
"""
Gửi tin nhắn Telegram từ một hook của Claude Code.

Cách gọi (trong command của hook, xem settings.json):
    python3 "$HOME/.claude/hooks/tele-notify.py" done     # hook Stop  -> báo xong
    python3 "$HOME/.claude/hooks/tele-notify.py" input    # hook Notification -> cần hỏi lại

File cấu hình (~/.claude/tele-notify.json):
    { "bot_token": "123456:ABC-DEF...", "chat_id": "123456789" }
Hoặc dùng biến môi trường TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID.
"""
import json
import os
import sys
import html
import urllib.request
import urllib.parse
from pathlib import Path


def load_config():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    cfg_path = Path.home() / ".claude" / "tele-notify.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text())
            token = token or cfg.get("bot_token")
            chat_id = chat_id or cfg.get("chat_id")
        except Exception as e:
            sys.stderr.write(f"tele-notify: config lỗi {cfg_path}: {e}\n")
    return token, (str(chat_id) if chat_id is not None else None)


def main():
    token, chat_id = load_config()
    if not token or not chat_id:
        sys.stderr.write("tele-notify: thiếu bot_token / chat_id\n")
        return 0  # luôn exit 0 để không chặn Claude

    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    kind = sys.argv[1] if len(sys.argv) > 1 else "done"
    cwd = data.get("cwd") or os.getcwd()
    project = html.escape(Path(cwd).name or cwd)

    def first(*keys):
        for k in keys:
            v = str(data.get(k, "")).strip()
            if v:
                return html.escape(v)
        return ""

    # StopFailure chưa có schema chính thức nên thử vài key khả dĩ, thiếu thì bỏ qua
    message = first("message", "reason", "error", "error_type")

    if kind == "input":
        text = f"❓ <b>Claude Code cần bạn xử lý</b>\n📁 {project}"
        if message:
            text += f"\n💬 {message}"
    elif kind == "limit":
        text = f"🚫 <b>Claude Code: đã chạm usage limit</b>\n📁 {project}"
        if message:
            text += f"\n⚠️ {message}"
        text += "\n⏳ Chờ tới lúc reset rồi chạy tiếp nhé."
    else:
        text = f"✅ <b>Claude Code đã hoàn thành</b>\n📁 {project}"

    api = f"https://api.telegram.org/bot{token}/sendMessage"
    body = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode()
    try:
        req = urllib.request.Request(api, data=body)
        urllib.request.urlopen(req, timeout=8)
    except Exception as e:
        sys.stderr.write(f"tele-notify: gửi thất bại: {e}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
