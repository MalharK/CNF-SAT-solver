# coding=utf-8
import copy

inferred_group_count = 0


def remove_key_dict(clause, literal, make_copy):
    """
    Removes from the dictionary the key *key* if present and returns the remaining dictionary
    :param clause: clause in the sentence
    :param literal: literal that needs to be removed from the clause
    :return: clause after removing the literal from the clause
    """
    if make_copy:
        updated_clause = copy.copy(clause)
        updated_clause.pop(literal, None)
        return updated_clause
    else:
        clause.pop(literal, None)
        return clause


def assign_value(cnf, literal, make_copy):
    """
    Assigns a symbol true value
    removes the clauses with the symbol and omits !symbol from the remaining clauses
    :param cnf: sentence in the cnf form that that has the literal *symbol* that needs to be assigned a value
    :param literal: literal that needs to be assigned True value in the cnf
    :return: new cnf after the assignment of the true value has been made to the literal
    """
    global inferred_group_count
    temp_cnf = [remove_key_dict(c, '-' + literal if literal[0] != '-' else literal[1:], make_copy) for c in cnf if
                literal not in c]
    if literal[0] == "-":
        return temp_cnf
    split_literal = literal.partition("_")
    for g in range(1, inferred_group_count + 1):
        if g != int(split_literal[2]):
            temp_cnf = assign_value(temp_cnf, "-" + split_literal[0] + "_" + str(g), False)
    return temp_cnf


def dpll(cnf):
    """
    Code for the dpl algorithm
    :param cnf: sentence in the cnf form [[clause], [clause],...]
                where clause is [literal, literal, literal]
                ex:[[literal, literal], [literal]]
                negation of literal is stated as -literal
    :return: True if resolution is possible else false and model of the assignments made
    """
    cnf = [{literal: True for literal in clause} for clause in cnf]
    # print len(cnf)
    model = set()
    # terminating conditions
    if len(cnf) == 0:
        return True, model
    if min(map(len, cnf)) == 0:
        return False, model
    # Checking pure literals
    # TODO: Optimize
    pure_dict = {}
    b_picker = {}
    for clause in cnf:
        for literal in clause:
            if literal in pure_dict:
                pure_dict[literal] += 1
            else:
                pure_dict[literal] = 1
            if literal in b_picker:
                b_picker[literal] += 1
            elif ('-' + literal if literal[0] != '-' else literal[1:]) in b_picker:
                b_picker[('-' + literal if literal[0] != '-' else literal[1:])] += 1
            else:
                b_picker[literal] = 1
    for literal in pure_dict:
        if not ('-' + literal if literal[0] != '-' else literal[1:]) in pure_dict:
            model.add(literal)
            evaluation, sub_model = dpll(assign_value(cnf, literal, False))
            return (evaluation, model) if evaluation is False else (evaluation, model | sub_model)
    # Checking unit literals
    for clause in cnf:
        if len(clause) == 1:
            [(k, v)] = clause.items()
            model.add(k)
            evaluation, sub_model = dpll(assign_value(cnf, k, False))
            return (evaluation, model) if evaluation is False else (evaluation, model | sub_model)
    # return after assign possible values to a variable
    # TODO: Pick a clause that has maximum presence
    # (k, v) = cnf[0].items()[0]

    k = max(b_picker, key=b_picker.get)

    evaluation, sub_model = dpll(assign_value(cnf, k, True))
    if evaluation:
        model.add(k)
        return evaluation, model | sub_model
    evaluation, sub_model = dpll(assign_value(cnf, '-' + k if k[0] != '-' else k[1:], False))
    if evaluation:
        model.add('-' + k if k[0] != '-' else k[1:])
        return evaluation, model | sub_model
    else:
        return evaluation, model


def read_file(filename):
    cnf = []
    f = open(filename, "r")
    for line in f:
        line = line.strip("\n").strip(" ")
        cnf.append(line.split(","))
    f.close()
    return cnf


def write_output(solvable, solution_set):
    cnf = []
    f = open("output.txt", "w")
    if solvable:
        for s in solution_set:
            f.write(s + " True\n")
        f.write("Unassigned variables can have any value")
    else:
        f.write("No valid assignments possible")
    f.close()


# dpll([['-a', '-c'], ['c', '-b'], ['a'], ['b']])
solvable, solution_set = dpll(read_file('input.txt'))
write_output(solvable, solution_set)
