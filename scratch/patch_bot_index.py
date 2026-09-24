import re

path = "src/index.ts"
with open(path, "r") as f:
    data = f.read()

data = data.replace("console.log(`[boot] chat         ${config.chatId}`);", "console.log(`[boot] chats        ${config.chatIds.join(', ')}`);")

with open(path, "w") as f:
    f.write(data)


path = "src/bot.ts"
with open(path, "r") as f:
    data = f.read()

notifier_func = """export function createNotifier(bot: Bot, config: BotConfig) {
  return async (text: string): Promise<void> => {
    await bot.api.sendMessage(config.chatId, text, {
      parse_mode: "MarkdownV2",
      link_preview_options: { is_disabled: true },
    });
  };
}"""

new_notifier_func = """export function createNotifier(bot: Bot, config: BotConfig) {
  return async (text: string): Promise<void> => {
    const results = await Promise.allSettled(
      config.chatIds.map(chatId => 
        bot.api.sendMessage(chatId, text, {
          parse_mode: "MarkdownV2",
          link_preview_options: { is_disabled: true },
        })
      )
    );

    const failures = results.filter((r) => r.status === "rejected") as PromiseRejectedResult[];
    if (failures.length > 0) {
      if (failures.length === config.chatIds.length) {
        throw failures[0].reason;
      } else {
        for (const failure of failures) {
          console.error(`[bot] partial delivery failure:`, failure.reason);
        }
      }
    }
  };
}"""

data = data.replace(notifier_func, new_notifier_func)
with open(path, "w") as f:
    f.write(data)

