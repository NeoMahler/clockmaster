from discord.ext import commands
import json

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def clean_game_state(self):
        """
        Cleans the game_state.json file.
        """
        starting_dictionary = {"players": {}, "day": {}, "night": {}, "status": "off"}
        with open("config/game_state.json", 'w') as f:
            json.dump(starting_dictionary, f)

    def read_game_state(self):
        """
        Reads the game_state.json file. Returns the entire dictionary.
        """
        with open("config/game_state.json", 'r') as f:
            state = json.load(f)
        return state

    def get_state_item(self, key):
        """
        Returns the value of a config item.

        Parameters:
            key (str): The name of the config item.
        """
        state = self.read_game_state()
        return state[key]
    
    def modify_state_item(self, key, value):
        """
        Modifies a config item.
        
        Parameters:
            key (str): The name of the config item.
            value (str): The new value of the config item.
        """
        state = self.read_game_state()
        state[key] = value
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)

    def add_player(self, player):
        """
        Adds a player to the game. It includes the user ID, username, and server-specific nickname.

        Parameters:
            player (discord.User): The user to add to the game.
        """
        state = self.read_game_state()
        state['players'][str(player.id)] = {}
        state['players'][str(player.id)]["username"] = player.name
        state['players'][str(player.id)]["nickname"] = player.nick
        state['players'][str(player.id)]["display_name"] = player.display_name
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)
        return
    
    def remove_player(self, player):
        """
        Removes a player from the game.

        Parameters:
            player (discord.User): The user to remove from the game.
        """
        state = self.read_game_state()
        del state['players'][str(player.id)]
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)
        return
    
    def get_player_data(self, ctx, type, players=[]):
        """
        Returns either the mention, username, display_name, or nickname of a player.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
            type (str): The type of data to return.
            players (list): A list of Discord user IDs.
        """
        data = []
        added_players = self.get_state_item("players")

        if players != []: # Create a list of players only for the specified user
            for player in added_players:
                if player in players:
                    user = ctx.guild.get_member(int(player))
                    data.append(self.sort_player_info(type, user))
        else: # Create list for all players added to the game
            for player in added_players:
                user = ctx.guild.get_member(int(player))
                data.append(self.sort_player_info(type, user))
        return data
    
    def sort_player_info(self, type, user):
        """
        Sorts the player information based on the given type.

        Parameters:
            type (str): The type of information to sort. Valid values are "mention", "username", "display_name", and "nickname".
            user (User): The user object containing the player information.
        """
        if type == "mention":
            return user.mention
        elif type == "username":
            return user.name
        elif type == "display_name":
            return user.display_name
        elif type == "nickname":
            if user.nick == None:
                return user.display_name
            else:
                return user.nick    
 
def setup(bot):
    bot.add_cog(UtilitiesCog(bot))