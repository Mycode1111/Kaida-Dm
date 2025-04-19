from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
from discord import app_commands
import os

keep_alive()

# ดึงโทเคนจาก Environment Variable
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # ตั้งกิจกรรมเป็น "Streaming" (แสดง YouTube หรือกิจกรรมอื่นๆ)
    activity = discord.Streaming(name="Kaida Dm💚", url="https://www.youtube.com/watch?v=bH3vMDK_Hn0")
    await bot.change_presence(status=discord.Status.online, activity=activity)  # เปลี่ยนสถานะเป็น Online
    
    print(f"✅ Logged in as {bot.user}")
    
    try:
        # ซิงค์คำสั่ง Slash ในระดับ Global
        synced = await bot.tree.sync()  # ซิงค์คำสั่งแบบ global
        print(f"🔁 Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Sync error: {e}")

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



# รันบอทด้วย Token ที่ดึงจาก Environment Variable
bot.run(token)
