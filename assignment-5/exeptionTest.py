
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