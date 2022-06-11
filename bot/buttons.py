from typing import List
import discord


class AskRoleButton(discord.ui.Button['AskRole']):
    def __init__(self, role: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=role)
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: AskRole = self.view
        if view.member.id != interaction.user.id:
            await interaction.response.send_message('La pregunta no es para vos!', ephemeral=True)
            return
        view.role = self.role
        await view.assign_member_role(interaction, self.role)


class AskRole(discord.ui.View):
    children: List[AskRoleButton]

    def __init__(self, member: discord.Member, content: str):
        super().__init__()
        self.member: discord.Member = member
        # self.role: str = None
        self.content: str = content
        self.add_item(AskRoleButton('Analytics Engineer'))
        self.add_item(AskRoleButton('Data Analyst'))
        self.add_item(AskRoleButton('Data Engineer'))

    
    async def assign_member_role(self, interaction: discord.Interaction, role: str):
        role_to_add = discord.utils.get(self.member.guild.roles, name=role)
        await self.member.add_roles(role_to_add)
        content = f'Demosle la bienvenida a <@{self.member.id}>, que se suma como {role}!'
        self.stop()
        await interaction.response.edit_message(content=content, view=None)
        