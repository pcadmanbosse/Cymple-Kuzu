def table(self, name: str):
    return TableAvailable(self.query + f' TABLE {name}')
