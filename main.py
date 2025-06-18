import discord
from discord.ext import commands
from discord.ext.commands import Bot

import re
import time
import datetime
from Levenshtein import distance

def ignore_formatting(str):
    result = re.sub(r"\s+", "", str)
    result = result.lower()
    return result

def match_ignore(str1, str2):
    str1_no_space = re.sub(r"\s+", "", str1)
    str2_no_space = re.sub(r"\s+", "", str2)
    str1_no_space = str1_no_space.lower()
    str2_no_space = str2_no_space.lower()
    return str1_no_space == str2_no_space

def close_match(str1, str2):
    return distance(str1, str2) <= 1

def time_elapsed():
    elapsed_time = datetime.timedelta(seconds=(time.time() - start_time))
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f'{int(hours):02} hrs | {int(minutes):02} mins | {int(seconds):02} secs'
    return formatted_time

BOT_TOKEN = # Insert Discord bot token here

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

started = False
solved_puzzles = {}
timestamps = {}


@client.event
async def on_ready():
    bot_status = client.get_channel(1338409929953906688)
    embed = discord.Embed(title="Bot started", description=f'{time.ctime(time.time())}', color=discord.Color.green())
    await bot_status.send(embed=embed)
    print(f'Bot Started ({client.user})')
    print(f'---------------------------------------------------------------------------------------------------------------------------------------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global started
    global start_time

    admin_role = "Game Master"
    valid_guess = "^guess\s+((1[0-2]|[1-9])|meta)\s+(.+)$"
    puzzle_hunt_url = "https://achew.notion.site/alice-in-rlp-puzzle-hunt"
    meta_puzzle_url = "https://achew.notion.site/the-heart-of-the-cards"
    reference_sheet_url = "https://bp6summer.bpuzzled.io/reference_sheet"
    puzzles = {
        1: {
            "name": "Puzzle 1 - Picture Perfect",
            "answer": "TEMPORAL",
            "difficulty": "3 of Spades",
            "emoji": "3-♤"
        },
        2: {
            "name": "Puzzle 2 - Tit for Tat",
            "answer": "DEAD MEAT",
            "difficulty": "5 of Spades",
            "emoji": "5-♤"
        },
        3: {
            "name": "Puzzle 3 - Go With the Flow",
            "answer": "SHIP",
            "difficulty": "9 of Spades",
            "emoji": "9-♤"
        },
        4: {
            "name": "Puzzle 4 - Logical Reasoning",
            "answer": "CHEMISTRY",
            "difficulty": "10 of Spades",
            "emoji": "10-♤"
        },
        5: {
            "name": "Puzzle 5 - Radio Static",
            "answer": "VOUCHER",
            "difficulty": "2 of Diamonds",
            "emoji": "2-♢"
        },
        6: {
            "name": "Puzzle 6 - Rewind Time",
            "answer": "DESSERTS",
            "difficulty": "4 of Diamonds",
            "emoji": "4-♢"
        },
        7: {
            "name": "Puzzle 7 - Brainteasers",
            "answer": "MONEY",
            "difficulty": "6 of Diamonds",
            "emoji": "6-♢"
        },
        8: {
            "name": "Puzzle 8 - Anagram This!",
            "answer": "REARRANGE",
            "difficulty": "Queen of Diamonds",
            "emoji": "Q-♢"
        },
        9: {
            "name": "Puzzle 9 - Bingo Night at the Match Factory",
            "answer": "RAINBOW",
            "difficulty": "7 of Clubs",
            "emoji": "7-♧"
        },
        10: {
            "name": "Puzzle 10 - A Very Cryptic Card",
            "answer": "BARRELS",
            "difficulty": "8 of Clubs",
            "emoji": "8-♧"
        },
        11: {
            "name": "Puzzle 11 - Spectral Shift",
            "answer": "PHYSICS",
            "difficulty": "Jack of Clubs",
            "emoji": "J-♧"
        },
        12: {
            "name": "Puzzle 12 - Brimming With Pride",
            "answer": "BISEXUAL",
            "difficulty": "King of Clubs",
            "emoji": "K-♧"
        },
        13: {
            "name": "META Puzzle - The Heart of the Cards",
            "answer": "HELD EVERMORE",
            "difficulty": "N/A",
            "emoji": "META"
        }
    }

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    solve_logs = client.get_channel(1361472551905394750)
    guess_logs = client.get_channel(1361472682054651991)
    leaderboards = client.get_channel(1338412673888555069)

    # Help Command
    if message.content == "!help":
        embed = discord.Embed(title="Commands", description=f'`!help` - Show the help page\n`!start` - Start the Puzzle Hunt (Must have "{admin_role}" role)\n`!end` - Ends the Puzzle Hunt (Must have "{admin_role}" role)\n`!links` - Displays links to the puzzle hunt and to the reference sheet\n`!info` - Displays current puzzle hunt info\n`guess <Question Number> <Answer>` - Submit an answer to a question', color=discord.Color.blue())
        await message.channel.send(embed=embed)


    # Start the Puzzle Hunt
    role = discord.utils.get(message.author.roles, name=admin_role)
    if message.content == "!start" and not started:
        if role is not None and role.name == admin_role:
            started = True
            start_time = time.time()
            embed = discord.Embed(title="Puzzle Hunt Started", description="Start time: " + str(time.ctime(start_time)), color=discord.Color.green())
            await message.channel.send(embed=embed)
            embed = discord.Embed(title="Puzzle Hunt Link", url=puzzle_hunt_url, color=discord.Color.blue())
            await message.channel.send(embed=embed)
            embed = discord.Embed(title="Reference Sheet Link", url=reference_sheet_url, color=discord.Color.blue())
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="You do not have the permissions to start the Puzzle Hunt", color=discord.Color.red())
            await message.channel.send(embed=embed)
    elif message.content == "!start" and started:
        embed = discord.Embed(title="The Puzzle Hunt was already started", color=discord.Color.red())
        await message.channel.send(embed=embed)

    # End the Puzzle Hunt
    role = discord.utils.get(message.author.roles, name=admin_role)
    if message.content == "!end" and started:
        if role is not None and role.name == admin_role:
            started = False
            embed = discord.Embed(title="Puzzle Hunt Ended", description=f'Start Time: {str(time.ctime(start_time))}\nEnd Time: {str(time.ctime(time.time()))}\nDuration: {time_elapsed()}', color=discord.Color.green())
            await message.channel.send(embed=embed)
            # Print Leaderboards
            for channel in solved_puzzles:
                # Solve Status
                embed = discord.Embed(title=f"{channel} Results", color=discord.Color.blue())
                result = ""
                for i in range(len(puzzles)):
                    if puzzles.get(i+1).get("name") in solved_puzzles.get(channel, []):
                        result += f'✅ {puzzles.get(i+1).get("emoji")} | {puzzles.get(i+1).get("name")}\n'
                    else: 
                        result += f'❌ {puzzles.get(i+1).get("emoji")} | {puzzles.get(i+1).get("name")}\n'
                embed.add_field(name="Solve Status", value=result, inline=False)
                # Solve Time
                result = ""
                for i in range (len(solved_puzzles.get(channel, []))):
                    result += f'{solved_puzzles.get(channel)[i]} - {timestamps.get(channel)[i]}\n'
                embed.add_field(name="Solve Time", value=result, inline=False)
                # Stats
                embed.add_field(name="Stats", value=f'Total Puzzles Solved: {len(solved_puzzles.get(channel))}/{len(puzzles)}', inline=False)
                await leaderboards.send(embed=embed)
        else:
            embed = discord.Embed(title="You do not have the permissions to stop the Puzzle Hunt", color=discord.Color.red())
            await message.channel.send(embed=embed)
    elif message.content == "!end" and not started:
        embed = discord.Embed(title="No active puzzle hunt session", color=discord.Color.red())
        await message.channel.send(embed=embed)

    # Display Puzzle Hunt Link
    if message.content == "!links" and started:
        embed = discord.Embed(title="Puzzle Hunt Link", url=puzzle_hunt_url, color=discord.Color.blue())
        await message.channel.send(embed=embed)
        embed = discord.Embed(title="Reference Sheet Link", url=reference_sheet_url, color=discord.Color.blue())
        await message.channel.send(embed=embed)
    elif message.content == "!links" and not started:
        embed = discord.Embed(title="No active puzzle hunt session", color=discord.Color.red())
        await message.channel.send(embed=embed)

    # Show info
    if message.content == "!info" and started:
        embed = discord.Embed(title="Puzzle Hunt Info", description=f'Start Time: {str(time.ctime(start_time))}\nTIme Elapsed: {time_elapsed()}', color=discord.Color.blue())
        await message.channel.send(embed=embed)
    elif message.content == "!info" and not started:
        embed = discord.Embed(title="No active puzzle hunt session", color=discord.Color.red())
        await message.channel.send(embed=embed)

    # Validate Guesses
    if started:
        if re.search(valid_guess, user_message):

            puzzle_num = ignore_formatting(user_message.split(" ", 2)[1])

            if puzzle_num == "meta":
                answer = puzzles.get(13).get("answer")
                name = puzzles.get(13).get("name")
                difficulty = puzzles.get(13).get("difficulty")
                emoji = puzzles.get(13).get("emoji")
                guess = ignore_formatting(user_message.split("meta", 1)[1])
            else:
                name = puzzles.get(int(puzzle_num)).get("name")
                answer = puzzles.get(int(puzzle_num)).get("answer")
                difficulty = puzzles.get(int(puzzle_num)).get("difficulty")
                emoji = puzzles.get(int(puzzle_num)).get("emoji")
                guess = ignore_formatting(user_message.split(puzzle_num, 1)[1])
            
            if (match_ignore(answer, guess)):
                if name in solved_puzzles.get(channel, []):
                    embed = discord.Embed(title="You have already solved this puzzle", description=f'Puzzle: {name}\nAnswer: {answer}\nDifficulty: **`{difficulty}`**\n', color=discord.Color.red())
                    await message.channel.send(embed=embed)
                else:
                    solved_puzzles.setdefault(channel, []).append(name)
                    timestamps.setdefault(channel, []).append(time_elapsed())
                    await message.add_reaction('✅')
                    embed = discord.Embed(title="Congratulations!", description=f'Puzzle: {name}\nAnswer: {answer}\nDifficulty: **`{difficulty}`**\n', color=discord.Color.green())                    
                    embed.add_field(name="Time Elapsed", value=f'{time_elapsed()}', inline=False)
                    msg = await message.channel.send(embed=embed)
                    await msg.pin()
                    await solve_logs.send(f'(`{time_elapsed()}`) {channel} | {emoji} | {name}')
                    await guess_logs.send(f'✅ (`{time_elapsed()}`) {username} | {channel} | {emoji} | {name} | {guess}')
                    print(f'✅ ({time_elapsed()}) {username} | {channel} | {emoji} | {name} | {guess}')
                    # Meta puzzle unlocking
                    if len(solved_puzzles.get(channel, [])) == 8:
                        embed = discord.Embed(title="Meta Puzzle", description="8 puzzles solved...meta puzzle unlocked!\nguess meta <Answer> to submit a guess for the meta puzzle", url=meta_puzzle_url, color=discord.Color.blue())
                        await message.channel.send(embed=embed)
                    # Runs if meta is solved (TODO TEST THIS CODE)
                    if puzzle_num == "meta":
                        embed = discord.Embed(title="Puzzle Hunt Completed!!!", description=f'Final time: {time_elapsed()}', color=discord.Color.gold())
                        await message.channel.send(embed=embed)
            else:
                await message.add_reaction('❌')
                if close_match(ignore_formatting(answer), ignore_formatting(guess)):
                    await guess_logs.send(f'🟡 (`{time_elapsed()}`) {username} | {channel} | {emoji} | {name} | {guess}')
                    print(f'🟡 ({time_elapsed()}) {username} | {channel} | {emoji} | {name} | {guess}')
                else:
                    await guess_logs.send(f'❌ (`{time_elapsed()}`) {username} | {channel} | {emoji} | {name} | {guess}')
                    print(f'❌ ({time_elapsed()}) {username} | {channel} | {emoji} | {name} | {guess}')

        elif message.content.startswith('guess'):
            embed = discord.Embed(title='Use the following syntax to submit answers:', description='`guess <Question Number> <Answer>`', color=discord.Color.red())
            await message.channel.send(embed=embed)
    elif not started and message.content.startswith('guess'):
        embed = discord.Embed(title="No active puzzle hunt session", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Run the bot
client.run(BOT_TOKEN)
