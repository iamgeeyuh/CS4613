input = []  # stores input


def setup():
    letters = {
        "c1": {0, 1},
        "c2": {0, 1},
        "c3": {0, 1},
        "c4": {1},
    }  # letters: (domain, constraints)

    variables = ["" for x in range(13)]  # xn's letter at index n-1

    input_file = open("input.txt", "r")

    # set domain
    # x9: {1}
    # x1, x5: {range(1, 10)}
    # x2...x4, x6...x8, x10...x13: {range(10)}

    xn = 0

    for i in range(3):
        line = input_file.readline().replace("\n", "").strip()
        input.append(line)

        for letter in line:
            if letter == variables[8] or xn == 8:
                letters[letter] = {1}
            elif letter in (variables[0], variables[4]) or xn in (0, 4):
                letters[letter] = {x for x in range(1, 10)}
            else:
                letters[letter] = {x for x in range(10)}
            variables[xn] = letter
            xn += 1

    input_file.close()

    # set constraints
    # x4 + x8 = 10*c1 + x13
    # c1 + x3 + x7 = 10*c2 + x12
    # c2 + x2 + x6 = 10*c3 + x11
    # c3 + x1 + x5 = 10*c4 + x10
    # c4 = x9

    constraints = {
        key: set() for key in letters.keys()
    }  # stores letter: set(constraints)

    # for each variable xi, add its constraints
    for i in range(len(variables)):
        if i == 8:
            constraints[variables[i]].add("c4")
        elif i in [0, 1, 2, 3]:
            constraints[variables[i]].add(variables[i + 4])
            constraints[variables[i]].add(variables[i + 9])
            constraints[variables[i]].add(f"c{4-i}")
            if i != 3:
                constraints[variables[i]].add(f"c{3-i}")
        elif i in [4, 5, 6, 7]:
            constraints[variables[i]].add(variables[i - 4])
            constraints[variables[i]].add(variables[i + 5])
            constraints[variables[i]].add(f"c{8-i}")
            if i != 7:
                constraints[variables[i]].add(f"c{7-i}")
        elif i in [9, 10, 11, 12]:
            constraints[variables[i]].add(variables[i - 9])
            constraints[variables[i]].add(variables[i - 5])
            constraints[variables[i]].add(f"c{13-i}")
            if i != 12:
                constraints[variables[i]].add(f"c{12-i}")

    # add length of constraints to letters map
    for key in constraints.keys():
        constraints[key].discard(key)
        letters[key] = (letters[key], constraints[key])

    return letters, variables


def search(answer, letters, variables):
    if len(letters) == 0:
        return answer

    var = select_variable(letters)
    values = order_domain(var, letters)
    for value in values:
        answer[var] = value
        # makes copy of current state
        curr = {
            key: (letters[key][0].copy(), letters[key][1].copy())
            for key in letters.keys()
        }
        # update domains after assignment
        for key in letters.keys():
            letters[key][1].discard(var)
            if key not in ("c1", "c2", "c3", "c4") and var not in (
                "c1",
                "c2",
                "c3",
                "c4",
            ):
                letters[key][0].discard(value)
        letters.pop(var)
        # if not consistent, revert changes and go to next value in domain
        if not is_consistent(letters, variables, answer):
            letters = curr
            answer.pop(var)
            continue
        # is consistent, search further
        res = search(answer, letters, variables)
        if res:
            return res
        # branch is not valid, revert changes
        letters = curr
        answer.pop(var)
    return False


def select_variable(letters):
    # MRV, sort by length of domain
    values = sorted(letters.keys(), key=lambda key: -len(letters[key][0]))
    res = [values.pop()]
    while len(values) + len(res) == 0 and len(letters[values[-1]][0]) == len(
        letters[res[-1]][0]
    ):
        res.append(values.pop())

    # degree, sort by length of constraints set
    res.sort(key=lambda key: len(letters[key][1]))
    return res[-1]


def order_domain(var, letters):
    return sorted(list(letters[var][0]))


def is_consistent(letters, variables, answer):
    # when every letter has been assigned, check that constraint equations are valid
    if len(letters) == 0:
        for i in range(len(variables)):
            if i == 8:
                if answer[variables[i]] != answer["c4"]:
                    return False
            if i in [0, 1, 2]:
                if (
                    answer[variables[i]] + answer[f"c{3-i}"] + answer[variables[i + 4]]
                    != 10 * answer[f"c{4-i}"] + answer[variables[i + 9]]
                ):
                    return False
            if i == 3:
                if (
                    answer[variables[i]] + answer[variables[i + 4]]
                    != 10 * answer[f"c{4-i}"] + answer[variables[i + 9]]
                ):
                    return False
            if i in [4, 5, 6]:
                if (
                    answer[variables[i]] + answer[variables[i - 4]] + answer[f"c{7-i}"]
                    != 10 * answer[f"c{8-i}"] + answer[variables[i + 5]]
                ):
                    return False
            if i == 7:
                if (
                    answer[variables[i]] + answer[variables[i - 4]]
                    != 10 * answer[f"c{8-i}"] + answer[variables[i + 5]]
                ):
                    return False
            if i in [9, 10, 11]:
                if (
                    answer[variables[i - 5]]
                    + answer[variables[i - 9]]
                    + answer[f"c{12-i}"]
                    != 10 * answer[f"c{13-i}"] + answer[variables[i]]
                ):
                    return False
            if i == 12:
                if (
                    answer[variables[i - 5]] + answer[variables[i - 9]]
                    != 10 * answer[f"c{13-i}"] + answer[variables[i]]
                ):
                    return False
    return True


def output(answer):
    output = open("output.txt", "w")
    if not answer:
        output.write("No solution")
    else:
        for line in input:
            for letter in line:
                output.write(str(answer[letter]))
            output.write("\n")
    output.close()


if __name__ == "__main__":
    letters, variables = setup()
    output(search({}, letters, variables))
