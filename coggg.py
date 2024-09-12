from bot import *
selected_member = None


class ButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="🚫", row=0, custom_id="block_button")
    async def block_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel
            if channel:
                if interaction.user.id != get_channel_owner(channel.id):
                    await interaction.response.send_message(embed=discord.Embed(description=
                                                                                "Вы не являетесь владельцем этого канала."
                                                                                ), ephemeral=True,
                                                            delete_after=3)
                    return
                users = channel.members
                options = [discord.SelectOption(label=user.display_name, value=str(user.id)) for user in users]
                mban = members_with_ban()
                users = [channel.guild.get_member(mem) for mem in mban]
                options += [discord.SelectOption(label=user.display_name, value=str(user.id)) for user in users]
                select = Select(
                    placeholder="Кого в Бан/Снять Бан:",
                    options=options
                )

                async def select_callback(interaction: discord.Interaction):
                    try:
                        selected_user_id = int(interaction.data["values"][0])
                        selected_user = channel.guild.get_member(selected_user_id)
                        if selected_user is not None:
                            if selected_user.id != get_channel_owner(channel.id):

                                is_ban = not is_member_ban(channel.id, selected_user_id)
                                update_member_ban(channel.id, selected_user_id, is_ban)
                                if is_ban:
                                    await channel.set_permissions(selected_user, overwrite=discord.PermissionOverwrite(send_messages=True, connect=True, speak=True))
                                    try:
                                        await selected_user.move_to(None)
                                    except:
                                        print("FF")
                                else:
                                    await channel.set_permissions(selected_user, overwrite=discord.PermissionOverwrite(send_messages=False, connect=False, speak=False))
                                    try:
                                        await selected_user.move_to(None)
                                    except:
                                        print("FF")
                                await interaction.response.send_message(embed=discord.Embed(
                                    description=f"{selected_user.mention} {' снят Бан' if is_ban else ' в Бане'}"),
                                                                        ephemeral=True, delete_after=3)
                            else:
                                await interaction.response.send_message(embed=discord.Embed(description=
                                                                                            "Вы являетесь владельцем этого канала."
                                                                                            ), ephemeral=True,
                                                                        delete_after=3)
                        else:
                            await interaction.response.send_message(
                                f"Пользователь {selected_user.mention} не найден.",
                                ephemeral=True,
                                delete_after=3)
                    except:
                        await interaction.followup.send(f"Пользователь {selected_user.mention} не найден.\n"
                                                        f"Или в канале больше 25 пользователей",
                                                        ephemeral=True, delete_after=3)

                select.callback = select_callback
                view = View()
                view.add_item(select)
                await interaction.response.send_message(view=view, ephemeral=True, delete_after=5)
        except:
            await interaction.response.send_message(embed=discord.Embed(description=
                "Вы должны находиться в голосовом канале, чтобы использовать эту команду."),
                ephemeral=True, delete_after=3)

    @discord.ui.button(emoji="➕", row=0, custom_id="limit_button")
    async def limit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel
            if channel:
                if interaction.user.id != get_channel_owner(channel.id):
                    await interaction.response.send_message(embed=discord.Embed(description=
                                                                                "Вы не являетесь владельцем этого канала."
                                                                                ),
                                                            ephemeral=True, delete_after=3)
                    return
                await interaction.response.send_message(embed=discord.Embed(description=
                                                                            'Введите новый лимит участников (от 0 до 99):\n'
                                                                            '(0: Без ограничения)'
                                                                            ),
                                                        ephemeral=True, delete_after=3)
                message = await bot.wait_for('message', check=lambda
                    m: m.author.id == interaction.user.id and m.channel.id == interaction.channel_id, timeout=60.0)
                try:
                    limit = int(message.content)
                    await message.delete()
                    if 0 <= limit <= 99:
                        # Обновляем значение user_limit в базе данных
                        update_channel_limit(channel.id, limit)

                        # Обновляем значение user_limit на сервере Discord
                        await channel.edit(user_limit=limit)

                        await interaction.followup.send(embed=discord.Embed(description=
                                                                            f"{message.author.mention}, новый лимит установлен: {limit}"
                                                                            ),
                                                        ephemeral=True, delete_after=3)
                    else:
                        await interaction.followup.send(embed=discord.Embed(description=
                                                                            'Недопустимое значение лимита. Допустимый диапазон: 0-99.'
                                                                            ),
                                                        ephemeral=True, delete_after=3)
                except ValueError:
                    await interaction.followup.send(embed=discord.Embed(description=
                                                                        'Некорректный ввод. Пожалуйста, введите число от 0 до 99.'
                                                                        ),
                                                    ephemeral=True, delete_after=3)
        except:
            await interaction.response.send_message(embed=discord.Embed(description=
                "Вы должны находиться в голосовом канале, чтобы использовать эту команду."),
                ephemeral=True, delete_after=3)

    @discord.ui.button(emoji="🔒", row=0, custom_id="close_button")
    async def close_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel
            if channel:
                if interaction.user.id != get_channel_owner(channel.id):
                    await interaction.response.send_message(embed=discord.Embed(description=
                                                                                "Вы не являетесь владельцем этого канала."
                                                                                ),
                                                            ephemeral=True, delete_after=3)
                    return
                is_open = not is_channel_open(channel.id)
                update_channel_open(channel.id, is_open)
                if is_open:
                    await channel.set_permissions(channel.guild.default_role, connect=True)
                else:
                    await channel.set_permissions(channel.guild.default_role, connect=False)
                await interaction.response.send_message(embed=discord.Embed(description=
                                                                            f"Комната {'открыта' if is_open else 'закрыта'}"
                                                                            ),
                                                        ephemeral=True, delete_after=3)
        except:
            await interaction.response.send_message(embed=discord.Embed(description=
                "Вы должны находиться в голосовом канале, чтобы использовать эту команду."),
                ephemeral=True, delete_after=3)

    @discord.ui.button(emoji="✍️", row=1, custom_id="rename_button")
    async def rename_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel
            if channel:
                if interaction.user.id != get_channel_owner(channel.id):
                    await interaction.response.send_message(embed=discord.Embed(description=
                                                                                "Вы не являетесь владельцем этого канала."
                                                                                ),
                                                            ephemeral=True, delete_after=3)
                    return
                await interaction.response.send_message(embed=discord.Embed(description=
                                                                            'Введите новое имя комнаты:'
                                                                            ),
                                                        ephemeral=True, delete_after=3)
                message = await bot.wait_for('message', check=lambda
                    m: m.author.id == interaction.user.id and m.channel.id == interaction.channel_id, timeout=60.0)
                new_name = message.content
                await message.delete()

                # Обновляем имя комнаты на сервере Discord
                await channel.edit(name=new_name)

                await interaction.followup.send(embed=discord.Embed(description=
                                                                    f"{message.author.mention}, имя комнаты изменено на: {new_name}"
                                                                    ),
                                                ephemeral=True, delete_after=3)
        except:
            await interaction.response.send_message(embed=discord.Embed(description=
                "Вы должны находиться в голосовом канале, чтобы использовать эту команду."),
                ephemeral=True, delete_after=3)

    @discord.ui.button(emoji="🏌", row=1, custom_id="kick_button")
    async def kick_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel
            if channel:
                if interaction.user.id != get_channel_owner(channel.id):
                    await interaction.response.send_message(embed=discord.Embed(description=
                                                                                "Вы не являетесь владельцем этого канала."
                                                                                ), ephemeral=True,
                                                            delete_after=3)
                    return
                users = channel.members
                options = [discord.SelectOption(label=user.display_name, value=str(user.id)) for user in users]
                select = Select(
                    placeholder="Кого кикнуть:",
                    options=options
                )
                async def select_callback(interaction: discord.Interaction):
                    try:
                        selected_user_id = int(interaction.data["values"][0])
                        selected_user = channel.guild.get_member(selected_user_id)
                        if selected_user is not None:
                            if selected_user.id != get_channel_owner(channel.id):
                                await selected_user.move_to(None)
                                await interaction.response.send_message(f"Пользователь {selected_user.mention} был кикнут.",
                                                                        ephemeral=True,
                                                                        delete_after=3)
                            else:
                                await interaction.response.send_message(embed=discord.Embed(description=
                                                                                            "Вы являетесь владельцем этого канала."
                                                                                            ), ephemeral=True,
                                                                        delete_after=3)
                        else:
                            await interaction.response.send_message(f"Пользователь {selected_user.mention} не найден.",
                                                                    ephemeral=True,
                                                                    delete_after=3)
                    except:
                        await interaction.followup.send(f"Пользователь {selected_user.mention} не найден.\n"
                                                        f"Или в канале больше 25 пользователей",
                                                        ephemeral=True, delete_after=3)
                select.callback = select_callback
                view = View()
                view.add_item(select)
                await interaction.response.send_message(view=view, ephemeral=True, delete_after=5)
        except:
            await interaction.response.send_message(embed=discord.Embed(description=
                "Вы должны находиться в голосовом канале, чтобы использовать эту команду."),
                ephemeral=True, delete_after=3)

    @discord.ui.button(emoji="🔇", row=1, custom_id="mute_button")
    async def mute_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel
            if channel:
                afkid = channel.guild.get_channel(afk_id)
                if interaction.user.id != get_channel_owner(channel.id):
                    await interaction.response.send_message(embed=discord.Embed(description=
                                                                                "Вы не являетесь владельцем этого канала."
                                                                                ), ephemeral=True,
                                                            delete_after=3)
                    return
                users = channel.members
                options = [discord.SelectOption(label=user.display_name, value=str(user.id)) for user in users]
                mmute = members_with_mute()
                users = [channel.guild.get_member(mem) for mem in mmute]
                options += [discord.SelectOption(label=user.display_name, value=str(user.id)) for user in users if not user.voice or user.voice.channel != channel]
                select = Select(
                    placeholder="Кого в мут/снять мут:",
                    options=options
                )

                async def select_callback(interaction: discord.Interaction):
                    try:
                        selected_user_id = int(interaction.data["values"][0])
                        selected_user = channel.guild.get_member(selected_user_id)
                        if selected_user is not None:
                            if selected_user.id != get_channel_owner(channel.id):

                                is_mute = not is_member_mute(channel.id, selected_user_id)
                                update_member_mute(channel.id, selected_user_id, is_mute)
                                await interaction.response.send_message(embed=discord.Embed(
                                    description=f"{selected_user.mention} {' снят мут' if is_mute else ' в муте'}"),
                                    ephemeral=True, delete_after=3)
                                if is_mute:
                                    await channel.set_permissions(selected_user, overwrite=discord.PermissionOverwrite(send_messages=True, connect=True, speak=True))
                                    try:
                                        await selected_user.move_to(afkid)
                                        await selected_user.move_to(channel)
                                    except:
                                        print("FF")
                                else:
                                    await channel.set_permissions(selected_user, overwrite=discord.PermissionOverwrite(send_messages=False, connect=True, speak=False))
                                    try:
                                        await selected_user.move_to(afkid)
                                        await selected_user.move_to(channel)
                                    except:
                                        print("FF")
                            else:
                                await interaction.response.send_message(embed=discord.Embed(description=
                                                                                            "Вы являетесь владельцем этого канала."
                                                                                            ), ephemeral=True,
                                                                        delete_after=3)
                        else:
                            await interaction.response.send_message(
                                f"Пользователь {selected_user.mention} не найден.",
                                ephemeral=True,
                                delete_after=3)
                    except:
                        await interaction.followup.send(f"Пользователь {selected_user.mention} не найден.\n"
                                                        f"Или в канале больше 25 пользователей",
                                                        ephemeral=True, delete_after=3)

                select.callback = select_callback
                view = View()
                view.add_item(select)
                await interaction.response.send_message(view=view, ephemeral=True, delete_after=5)
        except Exception as e:
            print("Произошла ошибка:", e)
            await interaction.response.send_message(embed=discord.Embed(description=
                "Вы должны находиться в голосовом канале, чтобы использовать эту команду."),
                ephemeral=True, delete_after=3)


class ButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_category()
    @commands.command()
    async def ewq(self, ctx):
        view = ButtonView()
        await ctx.send(embed = discord.Embed(title='Управление Румами',
                          description="🚫 — Бан/Разбан участника\n"
                                      "➕ — задать новый лимит участников\n"
                                      "🔒 — закрыть/открыть руму\n"
                                      "✍️ — изменить название румы\n"
                                      "🏌 — выгнать участника из румы\n"
                                      "🔇 — Мут/Анмут участника\n"), view=view)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: discord.Interaction):
        view = ButtonView()
        await view.interaction_check(interaction)

def setup(bot):
    bot.add_cog(ButtonCog(bot))
