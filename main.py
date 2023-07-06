from SimplexMethod import SimplexMethod


if __name__ == "__main__":
    inf = open('input.txt', 'r')
    # первая цифра отвечает за кол-во переменных, за кол-во Х-ов
    variables = int(inf.readline().strip())

    # вторая цифра отвечает за кол-во неравенств, все они должны быть приведены к виду <= и их коэф-ты записаны в файле
    inequalities = int(inf.readline().strip())

    print('Количество переменных: ', variables)
    print('Количество ограничений: ', inequalities)

    task = SimplexMethod(variables, inequalities)

    # третья строка должна содержать коэф-ты целевой функции (с этой функцией не надо производить никаких манипуляций)
    line = inf.readline().strip().split()
    task.add_objective_function(line)

    # все остальные строки содержат коэфициенты неравенств, приведеных к виду <=, константы остаются справа
    for i in range(inequalities):
        line = inf.readline().strip().split()
        task.add_inequality_function(line, i)
    inf.close()

    print(task.get_table())
    task.run_simplex_method()

    print("Максимум ", task.get_max())
    print("Он достигается в координатах ", task.get_max_args())
