def shorten(s, N=80):
    """
    Return short representation of string s.
    """
    if len(s) <= N:
        return s[:]
    else:
        l = (N - 5)/2
        return '{} ... {}'.format(s[:l], s[-l:])
