from bot import *

class Delete_ticket(View):
    def __init__(self, channel, role):
        super().__init__(timeout=None)
        self.channel = channel
        self.role = role

    @discord.ui.button(label="Удалить тикет", emoji="🗑️", style=discord.ButtonStyle.red, custom_id="delete_ticket")
    async def delete_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.channel.delete()
            await self.role.delete()


class Create_ticket(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Сделать заказ", emoji="🛒", style=discord.ButtonStyle.green, custom_id="create_tiket")
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        category_id = 1170040471893053441
        category = guild.get_channel(category_id)
        seller_id = 1173503059020750910
        seller = guild.get_role(seller_id)
        if not category:
            await interaction.response.send_message(embed=discord.Embed(description="Ошибка, обратитесь к @dblgq"),
                                                    ephemeral=True,
                                                    delete_after=3)

        # Создание роли для тикета
        role = await guild.create_role(name=f"Ticket Role {member.name}")

        # Создание канала для тикета
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
            seller: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(f'ticket-{member.name}', overwrites=overwrites, category=category)
        channel_mention = f"<#{channel.id}>"
        # Добавление роли пользователю
        await member.add_roles(role)
        await interaction.response.send_message(embed=discord.Embed(description=f"Канал создан: {channel_mention}"),
                                                ephemeral=True,
                                                delete_after=5)

        view = Delete_ticket(channel, role)

        # Отправка сообщения в канал тикета
        embed = discord.Embed(title=f'Тикет {member.name}', colour=0xFF0000)
        embed.add_field(name=f"Нажмите кнопку, чтобы удалить тикет:", value="Пожалуйста подождите продавца",
                        inline=True)
        embed.set_author(name="Ботяра®")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/924881929877217280/15ba66a5e22515fd468608d581da5118.png?size=1024")
        await channel.send(f"{seller.mention} {member.mention}")
        await channel.send(embed=embed, view=view)

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1173503059020750910)
    async def prices(self, ctx):
        view = Create_ticket()

        embed = discord.Embed(title="ворк 24/7(не точно)", colour=0xFF0000)
        embed.set_image(url="https://raw.githubusercontent.com/dblgq/jdmcars/main/headerr.png")
        await ctx.send(embed=embed)

        embed = discord.Embed(colour=0xFF0000)
        embed.set_image(url="https://raw.githubusercontent.com/dblgq/jdmcars/main/main1.png")
        await ctx.send(embed=embed)

        embed = discord.Embed(colour=0xFF0000)
        embed.set_image(url="https://raw.githubusercontent.com/dblgq/jdmcars/main/main2.png")
        await ctx.send(embed=embed)

        embed = discord.Embed(colour=0xFF0000)
        embed.set_image(url="https://raw.githubusercontent.com/dblgq/jdmcars/main/main3.png")
        await ctx.send(embed=embed)

        embed = discord.Embed(colour=0xFF0000)
        embed.set_image(
            url="https://raw.githubusercontent.com/dblgq/jdmcars/main/end.png")
        # embed.add_field(name="Discord Nitro Full", value="Month = 345 руб, 1700 тнг\nYear = 3.100 руб, 15.500 тнг", inline=True)
        # embed.add_field(name="Discord Nitro Basic", value="Month = 180 руб, 1000 тнг\nYear = 1.200 руб, 6.000 тнг", inline=True)
        # embed.add_field(name=" ", value="Нажмите кнопку, чтобы сделать заказ:", inline=False)
        # embed.set_author(name="Ботяра®")
        # embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/924881929877217280/15ba66a5e22515fd468608d581da5118.png?size=1024")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_role(1173503059020750910)
    async def oplata(self, ctx):
        qiwi_emoji = discord.utils.get(ctx.guild.emojis, id=1174130632922771467)
        kaspi_emoji = discord.utils.get(ctx.guild.emojis, id=1174129648037273681)
        binance_emoji = discord.utils.get(ctx.guild.emojis, id=1174130863773061180)
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name=f"{qiwi_emoji} Qiwi:", value="+7 708 512 10 98\n Оплата по киви стоит дороже на 50р",
                        inline=False)
        embed.add_field(name=f"{kaspi_emoji} Kaspi:", value="4400 4302 4737 6384\n Бекзат Қ.", inline=False)
        embed.add_field(name=f"{binance_emoji} Binance:", value="986 467 59\n Binance ID", inline=False)
        embed.set_author(name="Способы оплаты:")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: discord.Interaction):
        view = Create_ticket()
        await view.interaction_check(interaction)

def setup(bot):
    bot.add_cog(TicketSystem(bot))
