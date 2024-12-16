from itertools import combinations
import numpy as np


def input_info_vector():
    """ Ввод информационного вектора с проверкой корректности. """
    try:
        vector = input("Введите информационный вектор из 4 бит (например, 1 0 1 1): ").split()
        vector = [int(bit) for bit in vector]
        if len(vector) == 4 and all(bit in (0, 1) for bit in vector):
            return vector
        else:
            print("Некорректный ввод! Введите ровно 4 бита (0 или 1).")
    except ValueError:
        print("Некорректный ввод! Попробуйте снова.")


def cyclic_encode(info_vector, generator_polynomial):
    """ Кодирование циклическим кодом. """
    z = len(generator_polynomial) - 1
    extended_vector = info_vector + [0] * z
    remainder = np.polydiv(extended_vector, generator_polynomial)[1].astype(int) % 2
    remainder = np.pad(remainder, (len(extended_vector) - len(remainder), 0), constant_values=0)
    codeword = (np.array(extended_vector) ^ remainder).tolist()
    return codeword


def detect_error(codeword, generator_polynomial):
    """ Проверка синдрома ошибки. """
    _, remainder = np.polydiv(codeword, generator_polynomial)
    if 1 in remainder.astype(int) % 2:
        return True
    return False


def generate_error_vectors(n, error_weight):
    """ Генерация векторов ошибок с заданной кратностью. """
    error_vectors = []
    for positions in combinations(range(n), error_weight):
        error_vector = [0] * n
        for pos in positions:
            error_vector[pos] = 1
        error_vectors.append(error_vector)
    return error_vectors


def calculate_detection(codeword, generator_polynomial, n):
    """ Вычисление обнаруживающей способности кода. """
    table = []

    for error_weight in range(1, n + 1):
        error_vectors = generate_error_vectors(n, error_weight)
        detected_errors = 0

        for error_vector in error_vectors:
            received_vector = [(c ^ e) for c, e in zip(codeword, error_vector)]
            if detect_error(received_vector, generator_polynomial):
                detected_errors += 1

        detection_rate = (detected_errors / len(error_vectors)) * 100
        table.append((error_weight, len(error_vectors), detected_errors, detection_rate))

    return table


info_vector = input_info_vector()
generator_polynomial = [1, 0, 1, 1]  # Порождающий полином (x^3 + x + 1)
n = 7  # Длина кодового слова

codeword = cyclic_encode(info_vector, generator_polynomial)
print(f"Закодированный вектор: {codeword}")

results = calculate_detection(codeword, generator_polynomial, n)

# Вывод таблицы
print("\nРезультирующая таблица:")
print(f"{'Кратность ошибки':<18}{'Число ошибок':<18}{'Обнаружено ошибок':<20}{'Обнаруж. способность (%)':<18}")
print("-" * 84)

for row in results:
    error_weight, total_errors, detected, detection_rate = row
    print(f"{error_weight:<18}{total_errors:<18}{detected:<20}{detection_rate:<18.2f}")
