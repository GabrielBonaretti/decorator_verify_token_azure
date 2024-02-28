class User:
    def __init__(self, oid, name, preferred_username, roles):
        self._oid = oid
        self._name = name
        self._preferred_username = preferred_username
        self._roles = roles

    @property
    def oid(self):
        return self._oid

    @property
    def name(self):
        return self._name

    @property
    def preferred_username(self):
        return self._preferred_username

    @property
    def roles(self):
        return self._roles
    
    def __str__(self):
        return f"""        
        "oid": "{self._oid}",
        "name": "{self._name}",
        "preferred_username": "{self._preferred_username}",
        "roles": "{self._roles}",
        """