from teamMember import *
from pyllist import sllist


class CyclicTeamList:
    def __init__(self):
        self.members = sllist()

    def addMember(self, name, duty):
        member = TeamMember(name, duty)
        if not self.members:
            self.members.append(member)
            member.next = member
        else:
            first_member = self.members.first
            member.next = first_member
            self.members.append(member)

    def findMember(self, name_to_find):
        current_member = self.members.first
        while current_member:
            if current_member.value.name == name_to_find:
                return current_member.value
            current_member = current_member.next
        return None
