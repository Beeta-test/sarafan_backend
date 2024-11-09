class SequenceIterator:
    def __init__(self):
        self.current_num = 1
        self.repeat_count = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.repeat_count == 0:
            self.current_num += 1
            self.repeat_count = self.current_num
        self.repeat_count -= 1
        return self.current_num


def generate_sequence(n: int):
    if n < 0:
        raise ValueError('Число не должно быть орицательным!')
    iterator = SequenceIterator()
    return [next(iterator) for _ in range(n)]


print(generate_sequence(100))
