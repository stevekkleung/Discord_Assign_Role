# Discord_Assign_Role
This Discord bot will do the following: 
1. assign role based on a text file: names_and_roles.txt
2. after execute the command: ?role
   - bot will cycle all of the roles in the text file for the server
   - if the name in the text file does not have the role, it will be added.
   - it will also check existing members with the role, if the name not in the text file, the role will be removed.

example of the text file:
name, role 
name1#1111,role1 
name2#1112,role1 
name3#2113,role2 
name4#4114,role4 
