import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from flask import Flask
import threading
import os

# ----- Веб-сервер -----
app = Flask('')

@app.route('/')
def home():
    return "Бот работает и готов к бою!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# ----- Настройка Discord-бота -----
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

EMBED_COLOR = 0x83ff00  # Цвет рамки эмбеда

# ----------- Страницы заявки -----------
application_embeds = [
    discord.Embed(
        title="**MINECRAFT**",
        description=(
            "**1.** Сколько вам лет?\n"
            "**2.** Ваш ник?\n"
            "**3.** Как долго вы играете на проекте?\n"
            "**4.** Есть донат? Если да — какой?\n"
            "**5.** Чем вы будете полезны?\n"
            "**6.** Зачем вам клан?\n"
            "**7.** Играли ли вы когда-то с читами? Если да — когда и зачем?\n"
            "**8.** Какой баланс койнов, мононеток и сапфиров?\n"
            "**9.** Ваш уровень в PvP и PvE (из 10)?\n"
            "**10.** Сколько часов в день вы играете?\n"
            "**11.** Можете ли вы общаться в голосовом чате?\n"
            "**12.** Расскажите о себе"
        ),
        color=EMBED_COLOR
    ),
    discord.Embed(
        title="**PLANE CRAZY**",
        description=(
            "**1.** Сколько вам лет?\n"
            "**2.** Ваш ник?\n"
            "**3.** Как долго вы играете? (дни, часы)\n"
            "**4.** Сколько часов в день вы играете?\n"
            "**5.** Зачем вам клан?\n"
            "**6.** Чем вы будете полезны?\n"
            "**7.** Лучшие постройки (2–3 скрина)?\n"
            "**8.** Ваш уровень в строительстве и PvP (из 10)?\n"
            "**9.** Можете ли вы общаться в голосовом чате?\n"
            "**10.** Расскажите о себе"
        ),
        color=EMBED_COLOR
    )
]

# ----------- Страницы правил -----------
rules_embeds = [
    discord.Embed(
        title="**ПРАВИЛА ЧАТА**",
        description=(
            "1. оскорбления (мут 1 час)\n"
            "1.1 оскорбления родителей (мут 2 часа)\n"
            "1.2 порнография/шок контент (нᴇ ʙ ɴsꜰᴡ) (мут 3 часа)\n"
            "1.3 оскорбление администрации (мут 3 часа)\n"
            "1.4 спам (мут 4 часа)\n"
            "1.5 распространение файлов с ратниками/ɸиɯ ᴄᴄыᴧоᴋ (бан навсегда)\n"
            "1.7 попытка краша сервера (бан навсегда)\n"
            "1.8 выпрашивание админки/других ролей с правами (мут 30 минут)"
        ),
        color=EMBED_COLOR
    ),
    discord.Embed(
        title="**ОБЩИЕ ПРАВИЛА**",
        description=(
            "2. троллинг / буллинг участников клана (мут/кик)\n"
            "2.1 шутки без одобрения над тем, кем шутят (мут/кик)\n"
            "2.2 непослушание старшего по званию чем вас (замечание/кик)\n"
            "2.3 игра с софтом (кик)\n"
            "2..4 афкашерство (кик)\n"
            "2.5 тупизм (кик)"
        ),
        color=EMBED_COLOR
    ),
    discord.Embed(
        title="**ПРАВИЛА МАЙНКРАФТА**",
        description=(
            "3. попрашайничество (замечание/кик)\n"
            "3.1 воровство ресов (кик)\n"
            "3.2 наглость (кик)\n"
            "3.3 неисполнение обязанностей/договоренностей (замечание/кик)"
        ),
        color=EMBED_COLOR
    ),
    discord.Embed(
        title="**ПРАВИЛА PLANE CRAZY**",
        description=(
            "4. использование шредеров (замечание/кик)\n"
            "4.1 копирование построек у своих без согласия владельца (замечание/кик)\n"
            "4.2 бить своих (замечание/понижение/кик)"
        ),
        color=EMBED_COLOR
    ),
    discord.Embed(
        title="**ПРАВИЛА АДМИНИСТРАЦИИ**",
        description=(
            "5. мут не указавши причину (замечание)\n"
            "5.1 кик/бан за просто так (снятие с админки)\n"
            "5.2 использование админки в своих целях (снятие с админки)\n"
            "5.3 изменение сервера без одобрения овнера (снятие с админки)\n"
            "5.4 не исполнение обязательств (снятие с админки)\n"
            "5.5 выдача роли выше member-ов без одобрения овнера (снятие с админки)"
        ),
        color=EMBED_COLOR
    ),
    discord.Embed(
        title="**ПРАВИЛА ЛИДЕРОВ**",
        description=(
            "6. оффлайн/афк (снятие с лидерки)\n"
            "6.1 выдача ролей кроме member-ов и выше 3 elder-ов (замечание/снятие с лидерки)"
        ),
        color=EMBED_COLOR
    )
]

# ----------- Пагинатор -----------
class Paginator(View):
    def __init__(self, embeds: list[discord.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current = 0

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.green)
    async def prev_button(self, interaction: discord.Interaction, button: Button):
        self.current = (self.current - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.green)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        self.current = (self.current + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

# ----------- Команды -----------
@tree.command(name="заявка", description="Показать форму заявки")
async def заявка(interaction: discord.Interaction):
    await interaction.response.send_message(embed=application_embeds[0], view=Paginator(application_embeds), ephemeral=False)

@tree.command(name="правила", description="Показать правила сервера")
async def правила(interaction: discord.Interaction):
    await interaction.response.send_message(embed=rules_embeds[0], view=Paginator(rules_embeds), ephemeral=False)

# ----------- Запуск бота -----------
@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")
    try:
        synced = await tree.sync()
        print(f"🔁 Слэш-команды синхронизированы: {len(synced)}")
    except Exception as e:
        print(f"❌ Ошибка синхронизации: {e}")

# Запускаем веб-сервер и бота
keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
