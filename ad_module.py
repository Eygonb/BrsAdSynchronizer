import ldap3
import re
import configuration


class AdModule:
    connection: ldap3.Connection
    student_destination: str

    def __init__(self):
        domain_name = configuration.get_var('AD_DOMAIN_NAME')
        server = (ldap3.Server(configuration.get_var('AD_SERVER_IP'), get_info=ldap3.ALL))
        login = configuration.get_var('AD_USER_LOGIN')
        password = configuration.get_var('AD_USER_PASSWORD')
        self.connection = ldap3.Connection(server, user='%s\\%s' % (domain_name, login),
                                           password=password,
                                           authentication=ldap3.NTLM, return_empty_attributes=True)
        self.connection.bind()
        if not self.connection.bind():
            print('Failed to bind to the directory: {}'.format(self.connection.result))

        self.student_destination = configuration.get_var('AD_STUDENT_DESTINATION')

    def get_student(self, login, full_name, student_id):
        if login is not None:
            students = self.search_student('(sAMAccountName={})'.format(login))
        else:
            students = self.search_student('(displayName={})'.format(full_name))
            if len(students) > 1:
                students = list(filter(lambda s: re.search(str(student_id), s.description.value) is not None, students))
            elif len(students) < 1:
                students = self.search_student('(description=*{}*)'.format(str(student_id)))
        return students

    def search_student(self, search_filter):
        self.connection.search(search_base=self.student_destination, search_filter=search_filter,
                               attributes=['distinguishedName', 'description', 'displayName', 'sAMAccountName'])
        return self.connection.entries

    def move_student(self, student_dn: str, student_type: StudentType, new_student_ou: str):
        # проверка есть ли конечный ou через search
        if not self.connection.search(search_base=self.student_destination,
                                      search_filter='&(objectCategory=organizationalUnit)(ou={})'.format(
                                          new_student_ou)):
            # если нет - создание через add
            new_ou_attrs = {
                'objectClass': [b'top', b'organizationalUnit'],
                'ou': new_student_ou.encode('utf-8')
            }
            self.connection.add('OU={},{},{}'.format(new_student_ou, student_type.value, self.student_destination),
                                ['organizationalUnit'],
                                new_ou_attrs)
        # 3 is num of parts in dn that need to be removed to move a student to another status,
        # for example CN=student_cn,OU=1 курс,OU=Дневное обучение to CN=student_cn,OU=Отчисленные
        # for an empty new_student_ou
        ou_level_num = 3
        self.connection.modify_dn(dn=student_dn,
                                  relative_dn=student_type.value + ',' + student_dn.split(',')[-ou_level_num],
                                  new_superior=new_student_ou)