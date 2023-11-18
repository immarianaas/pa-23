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
                return abstract_int(-1)
            elif {sign1, sign2} == {sign.pos, sign.zero}:
                return abstract_int(1)
            elif {sign1, sign2} == {sign.pos, sign.neg}:
                return abstract_int()
            elif sign1 == sign.all or sign2 == sign.all:
                return abstract_int()
            else:
                return abstract_int("missing cases")

    def mul(self, val):
        sign1 = self.value
        sign2 = val.value
        if (sign.zero in {sign1, sign2}) and {sign1, sign2} <= {
            sign.zero,
            sign.pos,
            sign.neg,
            sign.all,
        }:
            return abstract_int(0)
        elif sign.all in {sign1, sign2}:
            return abstract_int()
        elif (sign1 == sign.neg and sign2 == sign.neg) or (
            sign1 == sign.pos and sign2 == sign.pos
        ):
            return abstract_int(1)
        elif {sign1, sign2} == {sign.neg, sign.pos}:
            return abstract_int(-1)
        else:
            return abstract_int("missing cases")

    def sub(self, val):
        sign1 = self.value
        sign2 = val.value
        if any(
            (
                sign1 == sign.all or sign2 == sign.all,
                sign1 == sign.neg and sign2 == sign.neg,
                sign1 == sign.pos and sign2 == sign.pos,
            )
        ):
            return abstract_int()
        elif sign1 == sign.zero and sign2 == sign.zero:
            return abstract_int(0)
        elif any(
            (
                sign1 == sign.zero and sign2 == sign.neg,
                sign1 == sign.pos and sign2 == sign.zero,
                sign1 == sign.pos and sign2 == sign.neg,
            )
        ):
            return abstract_int(1)
        elif any(
            (
                sign1 == sign.neg and sign2 == sign.zero,
                sign1 == sign.zero and sign2 == sign.pos,
                sign1 == sign.neg and sign2 == sign.pos,
            )
        ):
            return abstract_int(-1)

    def size(self) -> int:
        s = self.value
        if s == sign.neg:
            return -1
        elif s == sign.pos:
            return 1
        elif s == sign.zero:
            return 0
        else:
            return None

    def div(self, val):
        sign1 = self.value
        sign2 = val.value
