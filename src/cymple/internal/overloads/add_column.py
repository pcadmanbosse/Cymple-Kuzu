def add_column(name: str, type: str, primary_key: bool = False, default_value: any = None, if_not_exists: bool = True):
    query_part = f""" ADD{" IF NOT EXISTS" if if_not_exists else ""} {name} {type}{f""" DEFAULT {default_value}""" if default_value is not None else ""}{
                     " PRIMARY KEY" if primary_key else ""}"""
    return AddColumnAvailable(self.query + query_part)
