def path(self, ref_name: str):
    return MatchAvailable(self.query + f' {ref_name} =')
