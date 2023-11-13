from enum import Enum

sign = Enum(
    "sign", ["all", "none", "zero", "pos", "neg", "nonzero", "nonpos", "nonneg"]
)


class abstract_int:
    def __init__(self, i: int = None) -> None:
        if i == None:
            self.value = sign.all
        elif i == 0:
            self.value = sign.zero
        elif i < 0:
            self.value = sign.neg
        elif i > 0:
            self.value = sign.pos
        else:
            self.value = sign.none

    def __str__(self) -> str:
        return str(self.value.name)

    def add(self, val):
        sign1 = self.value
        sign2 = val.value
        if sign1 == sign2:
            return self
        else:
            if {sign1, sign2} == {sign.neg, sign.zero}:
                return sign.neg.name
            elif {sign1, sign2} == {sign.pos, sign.zero}:
                return abstract_int(1)
            elif {sign1, sign2} == {sign.pos, sign.neg}:
                return abstract_int(None)
        
            

    def mul(self, val):
        sign1 = self.value
        sign2 = val.value
        if sign1 == sign.zero or sign2 == sign.zero:
            return abstract_int(0)

    def sub(self, val):
        sign1 = self.value
        sign2 = val.value

    def div(self, val):
        sign1 = self.value
        sign2 = val.value

