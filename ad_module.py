import ldap3
import re
import configuration


class AdModule:
    connection: ldap3.Connection
    student_destination: str

    def __init__(self):
        self.domain_name = configuration.get_var('AD_DOMAIN_NAME')
        self.server = (ldap3.Server(configuration.get_var('AD_SERVER_IP'), get_info=ldap3.ALL))
        login = configuration.get_var("AD_USER_LOGIN")
        password = configuration.get_var("AD_USER_PASSWORD")
        self.connection = ldap3.Connection(self.server, user="%s\\%s" % (self.domain_name, login),
                                           password=password,
                                           authentication=ldap3.NTLM, return_empty_attributes=True)
        self.connection.bind()
        self.student_destination = configuration.get_var('AD_STUDENT_DESTINATION')

    def get_student(self, login, full_name, student_id):
        if login is not None:
            students = self.search_student('(sAMAccountName=' + login + ')')
        else:
            students = self.search_student('(displayName=' + full_name + ')')
            if len(students) > 1:
                students = list(filter(lambda s: re.search(str(student_id), s.description.value) is not None, students))
            elif len(students) < 1:
                students = self.search_student('(description=*' + str(student_id) + '*)')
        return students

    def search_student(self, search_filter):
        self.connection.search(search_base=self.student_destination, search_filter=search_filter,
                               attributes=['distinguishedName', 'description', 'displayName', 'sAMAccountName'])
        return self.connection.entries
