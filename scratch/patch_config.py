import re

path = "src/config.ts"
with open(path, "r") as f:
    data = f.read()

data = data.replace("chatId: string;", "chatIds: string[];")

chatId_func = """    chatId(name: string): string {
      const value = this.required(name);
      // Telegram chat ids are integers (channels/supergroups are negative).
      // A @channelusername also works for public channels, so both are allowed.
      if (value !== "" && !/^-?\\d+$/.test(value) && !/^@[A-Za-z0-9_]{4,}$/.test(value)) {
        problems.push(
          `${name} must be a numeric chat id (e.g. -1001234567890) or a @channelusername; got "${value}"`,
        );
      }
      return value;
    },"""

chatIds_func = """    chatIds(name: string): string[] {
      const value = this.required(name);
      if (value === "") return [];
      
      const ids = value.split(",").map(s => s.trim()).filter(s => s !== "");
      if (ids.length === 0) {
        problems.push(`${name} is required but not set`);
        return [];
      }
      for (const id of ids) {
        if (!/^-?\\d+$/.test(id) && !/^@[A-Za-z0-9_]{4,}$/.test(id)) {
          problems.push(
            `${name} must contain numeric chat ids or @channelusernames; got "${id}"`,
          );
        }
      }
      return ids;
    },"""

data = data.replace(chatId_func, chatIds_func)
data = data.replace('chatId: c.chatId("TELEGRAM_CHAT_ID"),', 'chatIds: c.chatIds("TELEGRAM_CHAT_ID"),')

with open(path, "w") as f:
    f.write(data)
