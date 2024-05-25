def pprint(title, bin_str):
    is_mod_8 = len(bin_str) % 8 == 0
    is_mod_128 = len(bin_str) % 128 == 0

    base_string = f"{bin_str[:8]}...{(len(bin_str) - 16):03d}...{bin_str[-8:]}"

    base_string = f"{base_string} ({len(bin_str):>5} BIT)"    

    if is_mod_8:
        base_string = f"{base_string} [IS MOD 8]"
    
    if is_mod_128:
        base_string = f"{base_string} [IS MOD 128]"

    print(f"{title:<20} - {base_string}")