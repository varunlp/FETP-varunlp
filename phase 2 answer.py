def print_pattern(n):

    s = "FORMULAQSOLUTIONS" * ((n // 16) + 1)

    l = len(s)

    count = 0


    upper_lines = n // 2 + n % 2
    lower_lines = n // 2


    for i in range(1, upper_lines+1):

        for j in range(upper_lines-i):
            print(" ", end="")

        for k in range(2*i-1):
            print(s[count], end="")

            count = (count + 1) % l
        print()


    for i in range(lower_lines, 0, -1):

        for j in range(upper_lines-i):
            print(" ", end="")

        for k in range(2*i-1):
            print(s[count], end="")

            count = (count + 1) % l
        print()


num_lines = int(input("Enter the number of lines for the design: "))
print_pattern(num_lines)
