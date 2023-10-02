
import staticInterpreter
print(staticInterpreter.interpretBytecode([
          {
            "offset": 0,
            "opr": "push",
            "value": {
              "type": "integer",
              "value": 4
            }
          },
          {
            "offset": 1,
            "opr": "push",
            "value": {
              "type": "integer",
              "value": 0
            }
          },
          {
            "offset": 2,
            "opr": "binary",
            "type": "int",
            "operant": "div"
          },
          {
            "offset": 3,
            "opr": "return",
            "type": "int"
          }
        ]))

print(staticInterpreter.interpretBytecode([
          {
            "offset": 0,
            "opr": "push",
            "value": {
              "type": "integer",
              "value": 3
            }
          },
          {
            "offset": 1,
            "opr": "store",
            "type": "int",
            "index": 1
          },
          {
            "offset": 2,
            "opr": "load",
            "type": "int",
            "index": 1
          },
          {
            "offset": 3,
            "opr": "load",
            "type": "int",
            "index": 1
          },
          {
            "offset": 4,
            "opr": "binary",
            "type": "int",
            "operant": "sub"
          },
          {
            "offset": 5,
            "opr": "store",
            "type": "int",
            "index": 1
          },
          {
            "offset": 6,
            "opr": "load",
            "type": "int",
            "index": 0
          },
          {
            "offset": 7,
            "opr": "load",
            "type": "int",
            "index": 1
          },
          {
            "offset": 8,
            "opr": "binary",
            "type": "int",
            "operant": "div"
          },
          {
            "offset": 9,
            "opr": "return",
            "type": "int"
          }
        ]))