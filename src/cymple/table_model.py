import re

class ExpressionMixin:
    def __formatted__(self, other):
        if isinstance(other, ExpressionMixin):
            return other
        elif isinstance(other, str) and self._type == str:  # noqa: E721
            return f"'{other}'"
        return other
    
    def __add__(self, other): return Expr(self, '+', self.__formatted__(other), self._type)
    def __radd__(self, other): return Expr(self.__formatted__(other), '+', self, self._type)
    def __mul__(self, other): return Expr(self, '*', self.__formatted__(other), self._type)
    def __rmul__(self, other): return Expr(self.__formatted__(other), '*', self, self._type)
    def __truediv__(self, other): return Expr(self, '/', self.__formatted__(other), self._type)
    def __rtruediv__(self, other): return Expr(self.__formatted__(other), '/', self, self._type)
    def __sub__(self, other): return Expr(self, '-', self.__formatted__(other), self._type)
    def __rsub__(self, other): return Expr(self.__formatted__(other), '-', self, self._type)
    def __lt__(self, other): return Expr(self, '<', self.__formatted__(other),self._type)
    def __le__(self, other): return Expr(self, '<=', self.__formatted__(other),self._type)
    def __gt__(self, other): return Expr(self, '>', self.__formatted__(other),self._type)
    def __ge__(self, other): return Expr(self.__formatted__(other), '<=', self,self._type)
    def __eq__(self, other): return Expr(self, '=', self.__formatted__(other),self._type)
    def __ne__(self, other): return Expr(self, '<>', self.__formatted__(other),self._type)
    def __and__(self, other): return Expr(self, 'AND', self.__formatted__(other),self._type)
    def __or__(self, other): return Expr(self, 'OR', self.__formatted__(other),self._type)

class Expr(ExpressionMixin):
    def __init__(self, left, op, right, type):
        self.left = left
        self.op = op
        self.right = right
        self._type = type

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

    
class Field(ExpressionMixin):
    def __init__(self, name: str, type_: type, alias=None):
        self._name = name
        self._type = type_
        self._alias = alias

    def __get__(self, instance, owner):
        if instance is None:
            # Accessed via class: just return the property name
            return self._name
        # Accessed via instance: bind alias
        aliased = Field(self._name, self._type)
        aliased._alias = instance.__alias__
        return aliased

    def __str__(self):
        return f"{self._alias}.{self._name}" if self._alias else self._name

    def __repr__(self):
        return str(self)

class TableModelMeta(type):
    def __new__(cls, name, bases, namespace):
        annotations = namespace.get('__annotations__', {})
        for attr_name, attr_type in annotations.items():
            if attr_name not in namespace:
                namespace[attr_name] = Field(attr_name, attr_type)
        return super().__new__(cls, name, bases, namespace)
    def __repr__(cls):
        return re.sub(r'([a-z])([A-Z])', r'\1_\2', cls.__name__).upper()


class TableModel(metaclass=TableModelMeta):
    __alias__: str = None

    def __repr__(self):
        
        return self.__alias__ if self.__alias__ is not None else re.sub(r'([a-z])([A-Z])', r'\1_\2', self.__class__.__name__).upper()

    def __init__(self, alias: str = None):
        self.__alias__ = alias
        annotations = self.__class__.__annotations__
        for name in annotations:
            setattr(self, name, Field(name, annotations[name], self.__alias__))

