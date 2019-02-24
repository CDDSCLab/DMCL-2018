from enum import Enum
Role = Enum('Role', ('Follower','Candidate','Leader','Null'))
RoleName={}
RoleName[Role.Follower]='Follower'
RoleName[Role.Candidate]='Candidate'
RoleName[Role.Leader]='Leader'
RoleName[Role.Null]='Null'

if __name__ == '__main__':
	a = Role.Follower
	print('Follower'==RoleName[a])