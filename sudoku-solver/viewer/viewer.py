class Viewer:
    def view(puzzle):
        for y, row in enumerate(puzzle):
            if y in [0,3,6]:
                print("---------------------")
            s = ""
            for x, cell in enumerate(row):
                if x in [0,3,6]:
                    s += "|"
                if isinstance(cell, int):
                    s += str(cell) + " "
                else:
                    s += "  "
            print(s + "|")
        print("---------------------")