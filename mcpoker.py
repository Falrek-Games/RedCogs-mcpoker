import logging
from typing import Literal
from datetime import timedelta
from math import floor

from databases import Database

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.data_manager import cog_data_path

log = logging.getLogger("red.yamicogs.mcpoker")

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class MCPoker(commands.Cog):
    """
    Play some Minecraft Stat Poker
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

        self.config.register_global(**{"schema": 0})
        

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # this cog does not store any user data
        pass
    
    async def cog_load(self):
        self.db = Database(f'sqlite+aiosqlite:///{cog_data_path(self)}/db')
        await self.db.connect()

        


    async def cog_unload(self):
        pass

    _mcpoker = discord.app_commands.Group(
        name="mcpoker",
        description="Play some Minecraft Stat Poker",
    )

    @_mcpoker.command(name="start")
    async def sp_start(self, interaction: discord.Interaction):
        """Start a session"""
        await interaction.response.send_message(f"Attention!! A new Minecraft Stat Poker session is starting soon")
        thread = await (await interaction.original_response()).create_thread(name="[PREPARING] MCPoker Session 1")
        
        embed = discord.Embed(color=discord.Colour.from_str("#5b8731"), title="MCPoker Session 1", description=f"This session will start in approximitaly <t:{floor((thread.created_at + timedelta(minutes=10)).timestamp())}:R>")
        msg = await thread.send(embed=embed)

        

    @_mcpoker.command(name="join")
    async def sp_start(self, interaction: discord.Interaction):
        """Join a session"""        
        await interaction.response.send_message("To join a session, simply add yourself to a thread that is prefixed with `[PREPARING]`", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_thread_member_join(self, t_member: discord.ThreadMember):
        if t_member.id == self.bot.user.id:
            return
        
        member = await self.bot.get_or_fetch_member(t_member.thread.guild, t_member.id)
        thread = t_member.thread

        
        