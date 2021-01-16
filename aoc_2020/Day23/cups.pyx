#cython: language_level=3


cdef class Cup:
    cdef:
        unsigned int _value
        Cup _next
        Cup _smaller_cup

    @property
    def value(self):
        return self._value

    @property
    def smaller_cup(self):
        return self._smaller_cup

    @smaller_cup.setter
    def smaller_cup(self, Cup smaller_cup):
        self._smaller_cup = smaller_cup

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, Cup next_cup):
        self._next = next_cup

    def __init__(self, unsigned int value, Cup smaller_cup = None, Cup next_cup = None):
        self._value = value
        self._next = next_cup
        self._smaller_cup = smaller_cup

    def __repr__(self):
        next_cup = None if self._next is None else self._next.value
        smaller_cup = None if self._smaller_cup is None else self._smaller_cup.value
        return f'{self.__class__.__name__}(value={self.value}, next={next_cup}, smaller_cup={smaller_cup})'


cdef class CupsCircle:
    cdef:
        Cup _current_cup
        Cup _largest_cup
        Cup _head
        Cup _tail

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, Cup cup):
        self._head = cup

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, Cup cup):
        self._tail = cup

    @property
    def current_cup(self):
        return self._current_cup

    @current_cup.setter
    def current_cup(self, Cup cup):
        self._current_cup = cup

    @property
    def largest_cup(self):
        return self._largest_cup

    @largest_cup.setter
    def largest_cup(self, Cup cup):
        self._largest_cup = cup

    def __init__(self, Cup head, Cup tail):
        self._head = head
        self._tail = tail

        if self._head is None and self._tail is not None:
            self._head = self._tail
            self._head.next = self._tail
            self._largest_cup = self._head
        elif self._head is not None and self._tail is None:
            self._tail = self._head
            self._head.next = self._tail
            self._largest_cup = self._head
        elif self._head is not None and self._tail is not None:
            self._head.next = self._tail
            self._tail.next = self._head
            if self._head.value > self._tail.value:
                self._largest_cup = self._head
            else:
                self._largest_cup = self._tail
        self._current_cup = self._head

    cpdef public void add(self, Cup cup):
        if self._head is None:
            self._head = cup
            self._tail = cup
            self._largest_cup = cup
            self._current_cup = cup
            cup.next = cup
        else:
            self._tail.next = cup
            self._tail = cup
            self._tail.next = self._head
            if self._largest_cup.value < cup.value:
                self._largest_cup = cup

    cpdef public unsigned int pop(self):
        cpdef Cup deleted
        if self._head is None:
            raise IndexError("Empty CircleQueue")
        else:
            deleted = self._head
            if self._largest_cup is self._head:
                self._largest_cup = self._head.smaller_cup
            self._head = self._head.next
            self._tail.next = self._head
            return deleted.value

    cpdef public void remove(self):
        self.pop()

    cpdef public void insert(self, Cup destination_cup, list added_cups):
        added_cups[2].next = destination_cup.next
        destination_cup.next = added_cups[0]
        if destination_cup is self._tail:
            self._tail = added_cups[2]

    cpdef public Cup get_cup_label(self, unsigned int value):
        cpdef Cup cup = self._head
        while cup is not None:
            if cup.value == value:
                return cup
            cup = cup.next
            if cup is self._head:
                raise KeyError(f"No cup with the label {value}")

    def __str__(self):
        cpdef list output = []
        cpdef Cup cup = self._head
        while cup is not None:
            output.append(str(cup.value))
            if cup.next is self._head:
                break
            cup = cup.next
        return ''.join(output)


cpdef CupsCircle extend_cups_circle(CupsCircle cups_circle, Cup prev_cup, size_t start, size_t end):
    cdef unsigned int i = start
    cpdef Cup cup
    while i < end:
        i += 1
        cup = Cup(value=i, smaller_cup=prev_cup)
        cups_circle.add(cup)
        # print(cup, prev_cup)
        prev_cup = cup
    return cups_circle


cpdef CupsCircle perform_moves(CupsCircle cups_circle, size_t num_moves=100):
    cdef size_t i, j
    cpdef Cup cup
    cpdef Cup destination_cup = None
    cpdef list picked_cups

    for i in range(num_moves):
        # print(str(cups_circle), cups_circle.current_cup)
        picked_cups = [cups_circle.current_cup.next]
        for j in range(2):
            cup = picked_cups[j].next
            picked_cups.append(cup)
        # print('picked_cups:', picked_cups)
        cups_circle.current_cup.next = picked_cups[2].next
        destination_cup = cups_circle.current_cup.smaller_cup
        cups_circle.current_cup = cups_circle.current_cup.next
        while True:
            # print('destination_cup:', destination_cup)
            if destination_cup is None:
                destination_cup = cups_circle.largest_cup
            if destination_cup not in picked_cups:
                break
            destination_cup = destination_cup.smaller_cup
        cups_circle.insert(destination_cup, picked_cups)
    return cups_circle


