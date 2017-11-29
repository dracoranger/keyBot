# keyBot 
Looks for game keys on discord and stores them to a file  
Specifically, it does it when people call !gib, so it doesn't scan for them across Discord.  

#### Installiation guide
1. Download  
2. Extract  
3. Pip install discord  
4. create robot.txt  
 4a. add api token  
 4b. add server  
 4c. add userlevel (not implemented yet)  
 4d. add keys storage (csv)  
 4e. add usedkeys storage (csv)  
5. Add the robot to your server  

##### What it does
1. By pms people can give the bot keys
2. It will give those keys to a specific channel  
3. !keylist prints a list of the keys in storage  
4. keeps track of old keys in case someone decides to delete them to be a dick  

##### What it does not do
1. gives the name of who sent the key, though that should be pretty obvious by who requests the key in the designated file
2. sets who can get a key by role  
3. Generates a configuration file  

##### Plans for the future
1. Fix what it does not do to what it does
