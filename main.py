from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import time

keep_alive()

# ดึงโทเคนจาก Environment Variable
token = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# สร้างคำสั่ง Slash สำหรับส่งข้อความ DM
@bot.tree.command(name="dm", description="ส่งข้อความ DM หาใครสักคน")
@app_commands.describe(user="ผู้รับ", message="ข้อความที่ต้องการส่ง")
async def dm(interaction: discord.Interaction, user: discord.User, message: str):
    allowed_users = [996447615812112546, 1144141941588627578]  # แทนด้วย Discord User ID ของคุณ

    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
        return

    try:
        await user.send(f"📩 ข้อความจาก {interaction.user.display_name}: {message}")
        await interaction.response.send_message(f"✅ ส่งข้อความหา {user.name} เรียบร้อยแล้ว", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ ส่งไม่ได้: {e}", ephemeral=True)

custom_messages = [
    "Kaida Dm ready!💚",
    "Made by wasd.",
]

@tasks.loop(seconds=5)  # เปลี่ยนข้อความทุก 10 วินาที
async def rotate_custom_activity():
    current_message = custom_messages[rotate_custom_activity.current_index]
    await bot.change_presence(
        activity=discord.CustomActivity(name=current_message),
        status=discord.Status.online
    )
    rotate_custom_activity.current_index = (rotate_custom_activity.current_index + 1) % len(custom_messages)

rotate_custom_activity.current_index = 0

@bot.event
async def on_ready():
    # รีเฟรชคำสั่งใหม่ให้กับ Discord API
    rotate_custom_activity.start()  # เริ่มหมุนข้อความ
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')


# รันบอทด้วย Token ที่ดึงจาก Environment Variable
bot.run(token)
