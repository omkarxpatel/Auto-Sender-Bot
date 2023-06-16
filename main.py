import discord
from colorama import Fore
from secretsVals import token, webhooks

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}{bot.user.name} is Online - Version: {discord.__version__}{Fore.RESET}")


class ConfirmButton(discord.ui.View):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):

        if interaction.user and interaction.user.id == self.auth:
            await interaction.response.send_message(
                "Sending to servers...", ephemeral=True
            )
            button.disabled = True
            self.stop()
            
        else:
            await interaction.response.send_message(
                "Only the owner of this command can respond", ephemeral=True
            )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user and interaction.user.id == self.auth:
            await interaction.response.send_message(
                "Not sending to servers", ephemeral=True
            )

            button.disabled = True
            self.stop()
        else:
            await interaction.response.send_message(
                "Only the owner of this command can respond", ephemeral=True
            )


@bot.event
async def on_message(message):
    if message.channel.id == 1119061663715430400:
        print(message.content)
        if message.author.id in [797258598819561502, 838974822288851005]:

                view = ConfirmButton(message.author.id)
                
                embed = discord.Embed(
                    title = "Send this message?",
                    description = message.content,
                    timestamp = discord.utils.utcnow()
                    )
                
                await message.channel.send(embed = embed, view = view, delete_after=10) 
                await view.wait()
                
                if view.confirm:
                    for webhook in webhooks:
                        webhook = discord.SyncWebhook.from_url(webhook)        
                        webhook.send(message.content)

try:
    bot.run(token)
finally:
    print("Bot is Now Offline 🛑")
    
