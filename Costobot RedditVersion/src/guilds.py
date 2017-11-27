import src.utils as utility

def moderator_dict(name,id):
    struct = {"Name" : name, 'ID' : id}
    return struct

class guilds:
    def __init__(self):
        self.guild_list = []
        self.error_que = []
      
    def check_permissions(self,moderator,guild):
        for guild_object in self.guild_list:
            if guild_object['ID'] == guild:
                moderators = guild_object['Moderators']
            
            for member in moderators:
                if member['ID'] == moderator:
                    return True
                
            return False

    def pre_elimenary_checks(self,name,guildID) -> bool:

        for guild in self.guild_list:
            if guildID == guild['ID']:
                self.error_que.append("This guild is already registered")

            if name == guild['Name']:
                self.error_que.append("Guild name already taken")

        if len(self.error_que) == 0:
            return True
        else:
            return False
    
    def new_guild(self, name, guildID, password, ownerID, owner_display_name):

        if self.pre_elimenary_checks(name,guildID) is False:
            return False

        guild = {}
        guild['Name'] = name
        guild['ID'] = guildID
        guild['Password'] = password
        guild['Moderators'] = [{"Name" : owner_display_name, "ID" : ownerID}]
        self.guild_list.append(guild)

        print("Guild < " + name + " > Created with ID: " + str(guildID) + utility.get_timespamp())
        return True
        
    def fetch_errors(self) -> list:
        errors = self.error_que
        self.error_que = []
        return errors

    def add_moderator_to_guild(self,targeted_guild,new_moderator_name, new_moderator_id):
        if self.check_permissions(new_moderator_id,targeted_guild) is False:
            self.error_que.append("You do not have permissions")
            return False

        for guild in self.guild_list:
            if guild['ID'] == targeted_guild:
                targeted_guild = guild
                break

        for moderator in targeted_guild['Moderators']:
            if new_moderator_id == moderator['ID']:
                self.error_que.append("Moderator already in the list")
                return False
        
        targeted_guild['Moderators'].append(moderator_dict(new_moderator.display_name,new_moderator.id))
        print("Added " + new_moderator_name + " with ID: " + new_moderator_id + " to guild " + targeted_guild['Name'] + utility.get_timespamp())
        return True