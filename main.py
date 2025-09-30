import os
import asyncio
import discord
from discord.ext import commands

# Importa la función keep_alive desde keep_alive.py
from keep_alive import keep_alive

# Configuración del bot y los intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    """Carga todas las extensiones (cogs) desde la carpeta cogs."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Cargado el cog: {filename}")
            except Exception as e:
                print(f"❌ Error al cargar el cog: {filename}\n{e}")

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está listo."""
    print(f'Bot iniciado como {bot.user.name}#{bot.user.discriminator}')
    await bot.change_presence(activity=discord.Game(name="tu estado aquí"))
    
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos.")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")
    print('---')

async def main():
    """Función principal para cargar cogs e iniciar el bot."""
    await load_cogs()
    
    # Inicia el servidor web antes de que el bot se conecte
    keep_alive()
    
    # Obtiene el token de las variables de entorno
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        raise ValueError("El token de Discord no está configurado. Añade la variable de entorno DISCORD_TOKEN.")
    
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
