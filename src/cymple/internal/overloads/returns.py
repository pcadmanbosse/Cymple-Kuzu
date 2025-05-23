
def return_literal(self, literal):
    ret = f' RETURN'
    if literal is not None:
        literal = str(literal)
        ret += f' {literal}'

    return ReturnAvailable(self.query + ret)


def return_mapping(self, mappings):
    if not isinstance(mappings, list):
        mappings = [mappings]

    ret = ' RETURN ' + \
        ', '.join(
            f'{mapping[0]} AS {mapping[1]}' if mapping[1] else mapping[0].replace(".", "_")
            for mapping in mappings)

    return ReturnAvailable(self.query + ret)
