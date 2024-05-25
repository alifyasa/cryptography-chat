import secrets

def generate_p_box(size: int) -> list[int]:
    numbers = list(range(size))

    p_box = []
    while numbers:
        choice = secrets.choice(numbers)

        p_box.append(choice)
        numbers.remove(choice)
    
    return p_box

def generate_inverse_p_box(p_box):
    inv_p_box = [0] * len(p_box)
    for idx, val in enumerate(p_box):
        inv_p_box[val] = idx
    return inv_p_box

def pprint(s_box, hex=False, width=8, height=8):
    for i in range(height):
        if hex:
            print(', '.join(f'{x:02x}' for x in s_box[i*width:(i+1)*width]), end=",\n")
        else:
            print(', '.join(f'{x:>2}' for x in s_box[i*width:(i+1)*width]), end=",\n")


def main():
    p_box = generate_p_box(64) # permutate bit
    print("P-BOX")
    pprint(p_box)

    inv_p_box = generate_inverse_p_box(p_box)
    print("INV P-BOX")
    pprint(inv_p_box)

if __name__ == "__main__":
    main()