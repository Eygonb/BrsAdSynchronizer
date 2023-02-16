import ldap3

domain_name = 'CS'
server = (ldap3.Server('192.168.1.209', get_info=ldap3.ALL))


def password_checker(login, password):
    try:
        connection = ldap3.Connection(server,
                                      user="%s\\%s" % (domain_name, login),
                                      password=password,
                                      authentication=ldap3.NTLM)
        return connection.bind()
    except:
        print("False")


def get_connection(login, password):
    return ldap3.Connection(server,
                            user="%s\\%s" % (domain_name, login),
                            password=password,
                            authentication=ldap3.NTLM)