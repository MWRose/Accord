import threading

class PasswordChecker: 
    # handles threading of loading dictionaries 
    def __init__(self, password):
        self.password = password
        self.load_black_list()

    # loading black list of 100k common passwords
    def load_black_list(self):
        self.black_list_dict = {}
        blacklist = open('common_passwords.txt', 'r', encoding='utf8')
        lines = blacklist.readlines()
        for line in lines:
            self.black_list_dict[line.strip()] = 0 
            
    # checking if the attempted password is in the loaded password blacklist
    def is_in_blacklist(self, password):
        if (password in self.black_list_dict):
            # weak
            return True
        else: 
            return False
   
    # checking if the attempted password is between 8 and 64 characters 
    def is_pass_length_ok(self, password):
        if (len(password) < 8 or len(password) > 64):
            # weak
            return False
        else:
            # strong
            return True

    # checking if the attempted password contains 3 or more repeated characters
    def is_char_not_repeated(self, password):
        for idx in range(0, len(password)-2):
            if password[idx] == password[idx+1] and password[idx+1] == password[idx+2]:
                return False
        return True    
    
    # checking if it only contains letters or numbers
    def is_pass_mixed(self, password): 
        return not(password.isalpha()) and not(password.isdecimal())

    # checks if password satisfies the following password strength tests. criteria are as follows. 
    # -- Is more than 8 characters but no more than 64 
    # -- Contains a mix of letters and numbers 
    # -- Is not an English word 
    # -- Is not one of the top 100k common passwords 
    def password_checker(self):
        if not self.is_pass_length_ok(self.password):
            return False
        elif (self.is_char_not_repeated(self.password) and self.is_pass_mixed(self.password) and  not(self.is_in_blacklist(self.password))):
            return True
        else: 
            return False

# main function for the executable
if __name__ == "__main__":  
    passwordChecker = PasswordChecker("test1234")
    print(passwordChecker.password_checker())