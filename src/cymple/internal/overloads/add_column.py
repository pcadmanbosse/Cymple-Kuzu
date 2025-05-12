def add_column(name: str, type: str, primary_key: bool = False, default_value: any = None, if_not_exists: bool = True):
    if_not_exists_part = " IF NOT EXISTS" if if_not_exists else ""
    default_part = f" DEFAULT {default_value}" if default_value is not None else ""
    primary_key_part = " PRIMARY KEY" if primary_key else ""
    query_part = f""" ADD{if_not_exists_part} {name} {type}{default_part}{primary_key_part}"""
    return AddColumnAvailable(self.query + query_part)
