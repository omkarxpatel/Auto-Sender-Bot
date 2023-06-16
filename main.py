import os
import discord
from colorama import Fore
from secrets import WEBHOOKS, BOT_TOKEN

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
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):

        if interaction.user and interaction.user.id == self.auth:
            await interaction.response.send_message(
                "Sending to servers...", delete_after=10
            )
            self.value = True
            self.stop()
            
        else:
            await interaction.response.send_message(
                "Only the owner of this command can respond", ephemeral=True
            )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user and interaction.user.id == self.auth:
            await interaction.response.send_message(
                "Not sending to servers", delete_after=10
            )

            self.value = False
            self.stop()
            

        else:
            await interaction.response.send_message(
                "Only the owner of this command can respond", ephemeral=True
            )


@bot.event
async def on_message(message):
    if message.channel.id == 1119061663715430400:
        if message.author.id in [797258598819561502, 838974822288851005]:

                view = ConfirmButton(message.author.id)
                
                embed = discord.Embed(
                    title = "Send this message?",
                    description = f"`Message Content:`\n\n{message.content}",
                    timestamp = discord.utils.utcnow(),
                    )
                
                await message.channel.send(embed = embed, view = view, delete_after=10) 
                await view.wait()
                
                count, error = 0,0
                if view.value is None:
                    message.channel.send("Timed out...", delete_after=10)
                    
                elif view.value:
                    for webhook in WEBHOOKS:
                        webhook = discord.SyncWebhook.from_url(webhook)      
                         
                        try: 
                            webhook.send(message.content)
                            count += 1
                        except:
                            error += 1    
                            
                    msg = f"Message content: {message.content}\n\nSuccessfully sent to {count} channels.\nFailed to send to {error} channels."   
                    await message.channel.send(msg, delete_after=10)
                    print(msg, "\n\n")
                    
                    await message.add_reaction("✅")     
                
                else:
                    await message.add_reaction("❌")     
                    
                for child in view.children:
                    child.disabled = True
                        
                    
try:
    bot.run(BOT_TOKEN)
finally:
    print("Bot is Now Offline 🛑")
    
