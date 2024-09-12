from bot import *


class Random_buttons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:recloz:1053655128235847770>", row=0, custom_id="random_button")
    async def random_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = bot.get_guild(guild_id)
        admin_role = guild.get_role(admin_role_id)
        if not admin_role in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(description="У вас нет прав."),
                                                    ephemeral=True,
                                                    delete_after=3)
            return
        global team11, team22
        team11, team22 = randomize_groups()
        view = Random_buttons()
        embed = embeds_random(team11, team22)
        await interaction.response.edit_message(embed=embed, view=view)


    @discord.ui.button(emoji="✅", row=0, custom_id="go_button")
    async def go_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = bot.get_guild(guild_id)
        admin_role = guild.get_role(admin_role_id)
        if not admin_role in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(description="У вас нет прав."),
                                                    ephemeral=True,
                                                    delete_after=3)
            return
        view = discord.ui.View()
        await interaction.response.edit_message(view=view)
        guild = bot.get_guild(guild_id)
        cat = discord.utils.get(guild.categories, id=category_team_id)

        voice1 = await guild.create_voice_channel("Тима #1", overwrites={
                            guild.default_role: discord.PermissionOverwrite(connect=True, speak=True)},
                                                     category=cat, user_limit=5, rtc_region=russia)
        for member in team11:
            try:
                await member.move_to(voice1)
            except:
                await interaction.followup.send(
                    embed=discord.Embed(description=f"{member.mention} нету в голосовом канале!"),
                    delete_after=3)

        voice2 = await guild.create_voice_channel("Тима #2", overwrites={
            guild.default_role: discord.PermissionOverwrite(connect=True, speak=True)},
                                                  category=cat, user_limit=5, rtc_region=russia)
        for member in team22:
            try:
                await member.move_to(voice2)
            except:
                await interaction.followup.send(
                    embed=discord.Embed(description=f"{member.mention} нету в голосовом канале!"),
                    delete_after=3)


class Buttons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:joincloz:1053659859687571587>", row=0, custom_id="join_button")
    async def join_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        user = interaction.user
        if user not in users:
            users.append(user)
            embed = embeds_start()
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(embed=discord.Embed(description="Вы добавлены в список."),
                                                    ephemeral=True,
                                                    delete_after=3)
        else:
            users.remove(user)
            embed = embeds_start()
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(embed=discord.Embed(description="Вас убрали из списка."),
                                                    ephemeral=True,
                                                    delete_after=3)

    @discord.ui.button(emoji="<:startcloz:1053655178810761226>", row=0, custom_id="start_button")
    async def start_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = bot.get_guild(guild_id)
        admin_role = guild.get_role(admin_role_id)
        if not admin_role in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(description="У вас нет прав."),
                                                    ephemeral=True,
                                                    delete_after=3)
            return
        if not users or len(users) % 2:
            await interaction.response.send_message(embed=discord.Embed(description="Ошибка:\n"
                                                                                    "Нечетное количество участников!"),
                                                    ephemeral=True,
                                                    delete_after=3)
            return
        team1, team2 = randomize_groups()
        view = Random_buttons()
        embed = embeds_random(team1, team2)
        await interaction.response.send_message(embed=embed, view=view)

    @discord.ui.button(emoji="<:clozclose:1053656315551031356>", row=0, custom_id="clear_button")
    async def clear_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = bot.get_guild(guild_id)
        admin_role = guild.get_role(admin_role_id)
        if not admin_role in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(description="У вас нет прав."),
                                                    ephemeral=True,
                                                    delete_after=3)
            return
        users.clear()
        embed = embeds_start()
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(embed=discord.Embed(description="Успешно очищено!"),
                                                ephemeral=True,
                                                delete_after=3)


class TeamMake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_category_teams()
    @commands.command()
    async def teamgenerate(self, ctx):
        view = Buttons()
        embed = embeds_start()
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: discord.Interaction):
        view = Buttons()
        await view.interaction_check(interaction)
        view2 = Random_buttons()
        await view2.interaction_check(interaction)


def setup(bot):
    bot.add_cog(TeamMake(bot))