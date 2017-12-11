import src.utils as utility
import pickle

def moderator_dict(name,id):
    struct = {"Name" : name, 'ID' : id}
    return struct

class member(object):
    def __init__(self,Name,ID):
        self.ID = ID
        self.Name = Name

class group(object):
    def __init__(self,Name,Password,Owner:member):
        self.Name = Name
        self.Password = Password
        self.Members = []
        self.Moderators = []
        self.Moderators.append(Owner)
        self.Members.append(Owner)

    def add_moderator(self,new_moderator : member):
        for already_moderator in self.Moderators:
            if already_moderator.ID == new_moderator.ID:
                return False
        self.Moderators.append(new_moderator)
        return True

    def add_member(self,new_member : member):
        for already_member in self.Members:
            if already_member.ID == new_member.ID:
                return False
        self.Members.append(new_member)
        return True

    def check_permissions(self, author_id):
        for moderator in self.Moderators:
            if moderator.ID == author_id:
                return True
        return False

class guilds(object):
    def __init__(self):
        self.group_list = []
        self.error_que = []

    def new_group(self,group : group):
        self.group_list.append(group)

    # GROUP UTILITY FUNCTIONS START

    def save(self):
        pickle_out = open('save_data.pickle', 'wb')
        pickle.dump(self.group_list, pickle_out)
        pickle_out.close()

    def load(self):
        pickle_in = open('save_data.pickle', 'rb')
        guild_data = pickle.load(pickle_in)
        self.group_list = guild_data
        pickle_in.close()
        return guild_data 
    
    def check_if_available(self, new_group):
        if len(self.group_list) == 0:
            return True
        for groups in self.group_list:
            if groups.Name == new_group.Name:
                return False
        return True

    def fetch_group(self, group_name, password):
        for groups in self.group_list:
            if groups.Name == group_name:
                if groups.Password == password:
                    return groups
                else:
                    self.error_que.append("Invalid Password")
                    return False
            self.error_que.append("Group not found")
        return False

    # GROUP UTILITY FUNTIONS END
    def fetch_errors(self) -> list:
        errors = self.error_que
        self.error_que = []
        return errors

    def register_group(self,owner_id, owner_name, group_name, group_password):
        owner = member(owner_name, owner_id)
        new_group = group(group_name,group_password,owner)
        if self.check_if_available(new_group) is False:
            self.error_que.append("Group name already taken")
            return False
        self.new_group(new_group)
        print("Group Created")
        return True

    def add_member(self, guild, password, member_name, member_id):
        targeted_group = self.fetch_group(guild,password)      
        if targeted_group is False:
            return False
        else:
            new_member = member(member_name,member_id)
            result = targeted_group.add_member(new_member)
            if result is False:
                self.error_que.append("Member already in group")
                return False
            else:
                return True

    def add_moderator(self,author_id,to_group,password,member_name,member_id):
        targeted_group = self.fetch_group(to_group,password)      
        if targeted_group is False:
            self.error_que.append("Group was not found")
            return False
        else:
            if targeted_group.check_permissions(author_id) is False:
                self.error_que.append("You do not have permissions")
                return False
        new_member = member(member_name,member_id)
        result = targeted_group.add_moderator(new_member)
        if result is False:
            self.error_que.append("Member already in group")
            return False
        else:
            return True
    
    def get_moderatorlist(self, group ,password):
        targeted_group = self.fetch_group(group,password) 
        if targeted_group is False:
            self.error_que.append("Group was not found")
            return False
        return targeted_group.Moderators
    
    def get_memberlist(self, group ,password):
        targeted_group = self.fetch_group(group,password) 
        if targeted_group is False:
            self.error_que.append("Group was not found")
            return False
        return targeted_group.Members