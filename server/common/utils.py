def atoi(s):
    import string
    for i, j in enumerate(s):
        if j not in string.digits:
            try:
                return int(s[:i])
            except:
                return 0
    if len(s) == 0:
        return 0
    return int(s)
