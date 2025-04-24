def new_query(self, name: str):
    return NewQueryAvailable(self.query + f';')
