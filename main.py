import discord
from discord.ext import commands

# CONFIGURACIÓN DE TOKEN
TOKEN = 'MTQ4ODY1NjcwMzUzOTkwODgxOQ.GmQwzp.KPwvHWxX_14FVu_CIU1utcCf38EXlRROmu0duc'

# IDs DE CONFIGURACIÓN
ID_CANAL_VERIFY = 1488659551128391897
ID_ROL_CLEAR = 1488659960790388916
ID_ROL_OWNER = 1488430624128630914
ID_ROL_48 = 1488435966300651560
ID_ROL_MUTED = 1488663230455877822

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True          
intents.reactions = True        

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# Verificación de Staff (Owner o Rol Clear)
def es_staff(ctx):
    user_roles_ids = [role.id for role in ctx.author.roles]
    return ID_ROL_CLEAR in user_roles_ids or ID_ROL_OWNER in user_roles_ids

@bot.event
async def on_ready():
    print(f'--- 48 Fg;bot ONLINE ---')
    channel = bot.get_channel(ID_CANAL_VERIFY)
    if channel:
        await channel.purge(limit=5) 
        
        # Embed con título 48Fg y miniatura a la derecha
        embed = discord.Embed(
            title="48Fg", 
            description="Reacciona con ✅ para obtener acceso al servidor de Da Hood.", 
            color=0x000000 
        )
        embed.set_thumbnail(url="https://i.postimg.cc/hvGY0HWQ/Gemini-Generated-Image-b28yfnb28yfnb28y-Photoroom.png") 
        embed.set_footer(text="recuerda lockearte para entrar jajaja")
        
        msg = await channel.send(embed=embed)
        await msg.add_reaction("✅")

# --- COMANDO .r (Busca en Display Name y Username) ---
@bot.command(name="r")
async def give_role_partial(ctx, nombre_parcial: str, role: discord.Role):
    if es_staff(ctx):
        nombre_parcial = nombre_parcial.lower()
        member = discord.utils.find(
            lambda m: (m.display_name and m.display_name.lower().startswith(nombre_parcial)) or 
                      (m.name and m.name.lower().startswith(nombre_parcial)) or
                      (m.global_name and m.global_name.lower().startswith(nombre_parcial)), 
            ctx.guild.members
        )
        
        if member:
            try:
                await member.add_roles(role)
                await ctx.send(f"✅ Rol **{role.name}** asignado a {member.mention}")
            except discord.Forbidden:
                await ctx.send("❌ Error de jerarquía: Sube mi rol arriba de los demás.")
        else:
            await ctx.send(f"❌ No encontré a nadie que empiece por '{nombre_parcial}'.")
    else:
        await ctx.send("❌ No tienes rango.")

# --- PANEL DE COMANDOS ---
@bot.command(name="commands")
async def list_commands(ctx):
    if es_staff(ctx):
        embed = discord.Embed(title="📜 Panel de Control - 48Fg", color=0x000000)
        embed.add_field(name="🏷️ Roles", value="`.r [nombre] @rol` - Busca por Display/User y da rol.", inline=False)
        embed.add_field(name="🧹 Limpieza", value="`.c [n]` - Borra mensajes del chat.", inline=True)
        embed.add_field(name="🔇 Mute", value="`.mute @user` / `.unmute @user`", inline=True)
        embed.add_field(name="Staff", value="`.kick @user` / `.ban @user`", inline=False)
        await ctx.send(embed=embed)

# --- MODERACIÓN (MUTE/UNMUTE CON INTERCAMBIO) ---
@bot.command()
async def mute(ctx, member: discord.Member):
    if es_staff(ctx):
        r48, rm = ctx.guild.get_role(ID_ROL_48), ctx.guild.get_role(ID_ROL_MUTED)
        if rm:
            if r48 in member.roles: await member.remove_roles(r48)
            await member.add_roles(rm)
            await ctx.send(f"🔇 **{member.display_name}** muteado y Rol 48 quitado.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if es_staff(ctx):
        r48, rm = ctx.guild.get_role(ID_ROL_48), ctx.guild.get_role(ID_ROL_MUTED)
        if rm in member.roles:
            await member.remove_roles(rm)
            if r48: await member.add_roles(r48)
            await ctx.send(f"🔊 **{member.display_name}** desmuteado y Rol 48 devuelto.")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason="No especificada"):
    if es_staff(ctx):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"👢 **{member.display_name}** expulsado.")
        except:
            await ctx.send("❌ Error de jerarquía.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No especificada"):
    if es_staff(ctx):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"🔨 **{member.display_name}** baneado.")
        except:
            await ctx.send("❌ Error de jerarquía.")

@bot.command(name="c")
async def clear(ctx, amount: int = 100):
    if es_staff(ctx):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Chat limpiado.", delete_after=3)

# --- ROLES POR REACCIÓN ---
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id: return
    if str(payload.emoji) == "✅" and payload.channel_id == ID_CANAL_VERIFY:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        if member:
            r48 = guild.get_role(ID_ROL_48)
            rv = discord.utils.get(guild.roles, name="Verificado")
            roles = [r for r in [r48, rv] if r]
            if roles: await member.add_roles(*roles)

bot.run(TOKEN)
