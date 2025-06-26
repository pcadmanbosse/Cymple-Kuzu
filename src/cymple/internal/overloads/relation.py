from typing import Union


def related(self, label: str | list[str], ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
    return RelationAvailable(self.query + self._directed_relation('none', label, ref_name, properties, min_hops, max_hops, shortest, **kwargs))


def related_to(self, label: str | list[str], ref_name: str = None, properties: str = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
    return RelationAvailable(self.query + self._directed_relation('forward', label, ref_name, properties, min_hops, max_hops, shortest, **kwargs))


def related_from(self, label: str | list[str], ref_name: str = None, properties: str = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
    return RelationAvailable(self.query + self._directed_relation('backward', label, ref_name, properties, min_hops, max_hops, shortest, **kwargs))


def _directed_relation(self, direction: str, label: str | list[str], ref_name: str = None, properties: str = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
    min_hops_str = '' if min_hops == -1 else str(min_hops)
    max_hops_str = '' if max_hops == -1 else str(max_hops)

    if isinstance(label, list):
        relation_type = "|".join([f':{l}' for l in label])
    else:
        relation_type = '' if label is None else f': {label}'
    relation_ref_name = '' if ref_name is None else f'{ref_name}'
    relation_properties = f' {{{Properties(properties).to_str(**kwargs)}}}' if properties else ''

    if min_hops == 1 and max_hops == 1:
        relation_length = ''
    else:
        relation_length = '*'
        if shortest and not (min_hops == 1 and max_hops == 1):
            if shortest == 'all':
                relation_length += " ALL SHORTEST "
            else:
                relation_length += " SHORTEST "

        if min_hops == max_hops:
            if min_hops != -1:
                relation_length += f'{min_hops_str}'
        else:
            relation_length += f'{min_hops_str}..{max_hops_str}'

    if relation_ref_name or relation_type or relation_length or relation_properties:
        relation_str = f'[{relation_ref_name}{relation_type}{relation_length}{relation_properties}]'
    else:
        relation_str = ''

    if direction == 'forward':
        return f'-{relation_str}->'
    if direction == 'backward':
        return f'<-{relation_str}-'

    return f'-{relation_str}-'


__all__ = ['related', 'related_to', 'related_from', '_directed_relation']
