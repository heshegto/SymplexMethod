from numpy import zeros


class SimplexMethod:
    """Решение задачи линейного программирования в каноническом виде"""
    # Канонический вид это когда:
    # 1) решается задача поиска максимума целевой функции
    #           a1 * x1 + .. + an * xn -> max
    # 2) неравенства принимают ввид <=
    #           b11 * x1 + .. + b1n * xn <= c1
    #                       ..
    #           bn1 * x1 + .. + bnn * xn <= cn
    # При добавлении коэффициэнтов в таблицу класса не надо производить никаких манипуляций с ними: так как они записаны
    # в каноническом виде так их и заносим в таблицу класса

    def __init__(self, variables: int, inequalities: int) -> None:
        """В функции инициализации создается таблица, которая необходима для решения ЛП"""
        self.iter = 0
        self.LeadingRow = 0  # Разрешающая строка
        self.LeadingColumn = 0  # Разрешающий столбец

        self.aVar = variables  # Amount of Variables
        self.aIne = inequalities  # Amount of Inequalities

        self.aRow = int(inequalities + 1)  # Amount of Rows
        self.aCol = int(variables + self.aRow)  # Amount of Columns
        self.table = zeros((self.aRow, self.aCol))  # Таблица необходимая для решения

    def add_objective_function(self, list_of_elements: list) -> None:
        """Добавляет коэффициенты целевой функции в таблицу"""
        for i in range(len(list_of_elements)):
            self.table[0][i] = -int(list_of_elements[i])

    def add_inequality_function(self, list_of_elements: list, row_num: int) -> None:
        """Добавляет коэффициенты и константу ОДНОГО неравенства в таблицу"""
        for i in range(self.aVar):
            self.table[row_num + 1][i] = int(list_of_elements[i])
        self.table[row_num + 1][self.aVar + row_num] = 1
        self.table[row_num + 1][-1] = int(list_of_elements[-1])

    def run_simplex_method(self) -> None:
        """Решает задачу"""
        while self.iter == 0:
            # Ищем минимальный элемент в целевой функции, чтобы найти разрешающий столбец
            min_el = [self.table[0][0], 0]
            for i in range(self.aRow):
                if self.table[0][i] < min_el[0] and self.table[0][i] < 0:
                    min_el[0] = self.table[0][i]
                    min_el[1] = i
            if min_el[0] >= 0:
                print('Текущее базисное решение оптимально!')
                self.iter = 1
            else:
                self.LeadingColumn = min_el[1]
                self._check_have_inf_solutions()

    def _check_have_inf_solutions(self) -> None:
        """Здесь вроде как ошибки, пока не понимаю в чем;("""
        p = 1
        for i in range(1, self.aRow):
            if self.table[i][self.LeadingColumn] > 0:
                p = 0
            else:
                print('Значение задачи ЛП не ограничено!')
                self.iter = 2
        if p != 1:
            min_el = [self.table[1][-1] / self.table[1][self.LeadingColumn], 1]
            for i in range(1, len(self.table)):
                if self.table[i][self.LeadingColumn] > 0:
                    a = self.table[i][-1] / self.table[i][self.LeadingColumn]
                    if min_el[0] > a:
                        min_el[0] = a
                        min_el[1] = i

            self.LeadingRow = min_el[1]
            self._change_table()

    def _change_table(self) -> None:
        """Меняет таблицу: делит, вычитает. Делает так, чтобы Разрешающий столбец стал базисом"""
        table = zeros((self.aRow, self.aCol))
        lead_el = self.table[self.LeadingRow][self.LeadingColumn]  # Leading element
        for i in range(self.aRow):
            if i != self.LeadingRow:
                for j in range(self.aCol-1):
                    table[i][j] = self.table[i][j] - (self.table[self.LeadingRow][j] / lead_el * self.table[i][self.LeadingColumn])
                table[i][self.aCol-1] = self.table[i][self.aCol-1] - (self.table[self.LeadingRow][self.aCol-1] / lead_el * self.table[i][self.LeadingColumn])
            else:
                for j in range(self.aCol - 1):
                    table[i][j] = self.table[i][j] / lead_el
                table[i][self.aCol-1] = self.table[i][self.aCol-1] / lead_el
        print(table)
        self.table = table

    def get_table(self):
        """Передает таблицу"""
        return self.table

    def get_max(self):
        """Выводит максимум"""
        if self.iter != 0:
            return self.table[0][-1]
        else:
            print("Сперва необходимо запустить метод")

    def get_max_args(self):
        """Выводит координаты максимума"""
        if self.iter != 0:
            result = list()
            for i in range(self.aRow):
                for j in range(self.aRow):
                    if self.table[j][i] == 1:
                        result.append(self.table[j][-1])
                        break
            return result
        else:
            print("Сперва необходимо запустить метод")
