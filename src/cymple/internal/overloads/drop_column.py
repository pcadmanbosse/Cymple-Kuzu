def drop_column(name: str, if_exists: bool = True):
    return DropColumnAvailable(self.query + f""" DROP {"IF EXISTS " if if_exists else ""}{name}""")
