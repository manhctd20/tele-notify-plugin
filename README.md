# tele-notify

Báo qua Telegram khi Claude Code:
- ✅ hoàn thành một lượt (Stop)
- ❓ cần bạn duyệt quyền / xử lý (Notification: permission_prompt)
- 🚫 chạm usage limit (StopFailure: rate_limit)

Dùng chung được cho cả CLI và app Desktop, vì cả hai đọc chung plugin đã cài.

## Cài (chạy trên MỖI máy, 1 lần)

```
/plugin marketplace add manhctd20/tele-notify-plugin
/plugin install tele-notify@my-tools
```

## Cấu hình token (mỗi máy làm 1 lần, KHÔNG đưa vào repo)

Tạo file `~/.claude/tele-notify.json`:

```json
{ "bot_token": "123456:ABC-DEF...", "chat_id": "123456789" }
```

Lấy token: nhắn @BotFather trên Telegram -> /newbot.
Lấy chat_id: nhắn bot 1 câu rồi mở https://api.telegram.org/bot<TOKEN>/getUpdates

## Cập nhật sau này

Sửa code trong repo -> push lên GitHub -> mỗi máy chạy:
```
/plugin marketplace update my-tools
```
