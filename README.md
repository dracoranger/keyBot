# keyBot 
Looks for game keys on discord and stores them to a file  
Specifically, it does it when people call !gib, so it doesn't scan for them across Discord.  

#### Installiation guide
1. Download  
2. Extract  
3. Pip install discord  
4. create robot.txt  
 4a. add api token  
 4b. add upper level keys storage (csv)  
 4c. add lower level keys storage (csv)  
 4d. add usedkeys storage (csv)   
 4e. add upper server  
 4f. add lower server  
 4g. add time to move from upper to lower 
 4h. add userlevel (not implemented yet)  
5. Add the robot to your server   

##### What it does
1. By pms, people can give the bot keys
2. It will give those keys to a specific channel  
3. !keylist prints a list of the keys in storage  
4. keeps track of old keys in case someone decides to delete them to be a dick  
5. gives the name of who sent the key
6. one key per day
7. keeps track of who gave the key
8. can ask for keys in uppercase or lowercase
9. NEW - added a two tier system
  9a. after a given amount of time, the keys are shifted from the upper to the lower
  9b. you can grab as many keys as you want from the lower

##### What it does not do
1. sets who can get a key by role  
2. Generates a configuration file  

##### Plans for the future
1. Move what it does not do to what it does
