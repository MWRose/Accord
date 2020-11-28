import shlex

class Command:
    def __init__(self, command):
        self.command = command
        self.parts = shlex.split(command)

    def is_logout(self):
        return self.command == ":logout"

    def is_add_contact(self):
        if not self.command.startswith(":add"):
            return False
        return self.__command_has_n_parts(2)

    def is_new_group(self):
        if not self.command.startswith(":newGroup"):
            return False
        return self.__command_has_n_parts(3)

    def is_direct_message(self):
        if not self.command.startswith(":direct"):
            return False
        return self.__command_has_n_parts(3)

    def is_group_message(self):
        if not self.command.startswith(":group"):
            return False
        return self.__command_has_n_parts(3)

    def is_list_contacts(self):
        return self.command == ":contacts"

    def is_list_groups(self):
        return self.command == ":groups"
    
    def is_group_info(self):
        if not self.command.startswith(":groups info"):
            return False
        return self.__command_has_n_parts(2)

    def is_block(self):
        # TODO
        return False

    def is_help(self):
        return self.command == ":help"

    def __command_has_n_parts(self, n):
        return len(self.parts) == n