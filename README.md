# Accord

### Secure and anonymous communication between multiple people over a network


Cryptography features implemented using Pycryptodome: https://pycryptodome.readthedocs.io/en/latest/src/signature/signature.html

## Running the Program

### Dependencies
- pycryptodome
- pyfiglet

### Scripts
- Direct Messaging: run script scripts/run.sh with the command  
``./run.sh [hostname] [server_port] [ca_port]``
- Group Messaging: run script scripts/run_group.sh with the command  
``./run_group.sh [hostname] [server_port] [ca_port]``
- Reseting keys and data base: run scrip scripts/reset.sh with the command  
``./reset.sh``

### General Use
In the ``/src`` folder you can find each of these command line programs

- Server.py: The server that relays messages and information between clients  
``python3 Server.py [server_port]``
- CA.py: The Certificate Authority that will create signatures for the user's public keys  
``python3 CA.py [ca_port]``
- Client.py: The main user interface. Here the client can create an account and loggin, as well as send and receive messages  
``python3 CA.py [host_name] [server_port] [ca_port]``

CA.py and Server.py need to be running before Client.py clients are added to the network.

Client.py command line interface

- ``:help`` for a list of commands
- NOTE: the ``>`` symbol must appear before writting a command (press enter if not present)
- NOTE: Contacts must be added before sending a message


### Storage
The database and keys are stored locally, so some storage must be free for these to be saved. 


