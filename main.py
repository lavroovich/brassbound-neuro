import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Настройка OpenAI клиента
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1/chat/completions",
    api_key=os.getenv("API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='#', intents=intents)

async def ask_deepseek(question, user_name):
    try:
        # Системный промпт с именем пользователя
        system_prompt = f"""Ты - бот на Discord-сервера Minecraft SMP сервера Brassbound. 
        Отввечай дружелюбно, допускается ненормативная лексика. Пользователь {user_name} задаёт тебе вопрос"""
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

@bot.command()
async def ai(ctx, *, question):
    user_name = ctx.author.name
    answer = await ask_deepseek(question, user_name)
    await ctx.send(f"**Вопрос от {user_name}:** {question}\n\n**Ответ:** {answer}")

# Запуск бота
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))