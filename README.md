# CNF-SAT-solver
Generates valid solution for a CNF_SAT if exists.
Read more about the SAT problem and CNF notation [here](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem).

Uses the [dpll](https://en.wikipedia.org/wiki/DPLL_algorithm) algorithm to generate solution if one exists.
### Setup
    #specify the cnf in input.txt
    #output generated in output.txt
    python dpll.py

### Input Format

> Each clause of the cnf should be specified on a new line.
> Each clause should consist of comma separated literals.
> Negation of literals should be represented by '-' prior to the pure literal. 
> (Ex: A and -A)

##### Example 'input.txt'

    A,B,C
    -A,-B,C
    A,-B,-C
    -A,B,-C
  
  This represents the CNF:

> ( A v B v C ) ^ ( ~A v ~B v C ) ^ ( A v ~B v ~C ) ^ (~ A v B v ~C)

### Output Format

> Specifies if valid assignment exists
> If yes, will specify the variable to be set, that is set to be True.
> The remaining variables can have any assignment
