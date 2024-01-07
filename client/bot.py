import discord, os, openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

clientAI = OpenAI(
    api_key=api_key,
)

#crear clase del bot de discord
class MyClient(discord.Client):
    #sobreescribir metodo on_ready
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
    

    async def on_message(self, message):
        # No permitas que el bot responda a sus propios mensajes
        if message.author == self.user:
            return
        
        if message.content.startswith('$ping'):
            latency = self.latency * 1000
            await message.channel.send(f'Pong! {int(latency)}ms')

        if message.content.startswith('$stats'):
            embed = discord.Embed(title="Estadísticas", description="Estadísticas del bot", color=0xeee657)
            embed.add_field(name="Usuarios", value=f"{len(self.users)}")
            embed.add_field(name="Servidores", value=f"{len(self.guilds)}")
            await message.channel.send(embed=embed)
        
        if message.content.startswith('$help'):
            embed = discord.Embed(title="Comandos", description="Lista de comandos del bot", color=0xeee657)
            embed.add_field(name="$ping", value="Muestra el ping del bot")
            embed.add_field(name="$stats", value="Muestra las estadísticas del bot")
            embed.add_field(name="$ask", value="Preguntale algo al bot")
            embed.add_field(name="$help", value="Muestra la lista de comandos")
            await message.channel.send(embed=embed)

        if self.user.mentioned_in(message):
            await message.channel.send(f'Hola {message.author.mention}! Mi prefijo es `$`')
        
        if message.content.startswith('$ask'):
            question = message.content[len('$ask '):]
            prompt = {
                "role": "user",
                "content": f"{question}"
            }

            try:
                # Llama a la API de OpenAI para obtener la respuesta
                await message.channel.send("Pensando...")
                chat_completion = clientAI.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[prompt],
                    stream=False,
                )

                response_message = chat_completion.choices[0].message.content
                await message.channel.send(response_message)
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send("Lo siento, ocurrió un error al procesar tu pregunta.")

    
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name='general')
        await channel.send(f'Bienvenido {member.mention}!')

    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name='general')
        await channel.send(f'Adios {member.mention}!')

global client
client = MyClient(intents=discord.Intents.all())
