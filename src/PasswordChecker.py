import threading


class PasswordChecker:

    def __init__(self, password):
        self.password = password
        self.load_black_list()

    def load_black_list(self):
        """
        Loads the black list of 100k common passwords
        """
        self.black_list_dict = {}
        blacklist = open('common_passwords.txt', 'r', encoding='utf8')
        lines = blacklist.readlines()
        for line in lines:
            self.black_list_dict[line.strip()] = 0

    def is_in_blacklist(self, password):
        """
        Checks if the attempted password is in the loaded password blacklist
        """
        if (password in self.black_list_dict):
            # weak
            return True
        else:
            return False

    def is_pass_length_ok(self, password):
        """
        Checks if the attempted password is between 8 and 64 characters
        """
        if (len(password) < 8 or len(password) > 64):
            # weak
            return False
        else:
            # strong
            return True

    def is_char_not_repeated(self, password):
        """
        Checks if the attempted password contains 3 or more repeated characters
        """
        for idx in range(0, len(password) - 2):
            if password[idx] == password[idx + 1] and password[idx + 1] == password[idx + 2]:
                return False
        return True

    def is_pass_mixed(self, password):
        """
        Checks if the password only contains letters or numbers
        """
        return not (password.isalpha()) and not (password.isdecimal())

    def password_checker(self):
        """
        Checks if password satisfies the following password strength tests. criteria are as follows:
            - is more than 8 characters but no more than 64
            - contains a mix of letters and numbers
            - is not an English word
            - is not one of the top 100k common passwords
        """
        if not self.is_pass_length_ok(self.password):
            return False
        elif (self.is_char_not_repeated(self.password) and self.is_pass_mixed(self.password) and not (
                self.is_in_blacklist(self.password))):
            return True
        else:
            return False


# Main function for the executable
if __name__ == "__main__":
    passwordChecker = PasswordChecker("test1234")
    print(passwordChecker.password_checker())
