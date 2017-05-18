
# Simple decorator

# def spam(func):
#     def wrapper(*args, **kwargs):
#         for i in range(10):
#             func(*args, **kwargs)
#     return wrapper
#
# @spam
# def sing(line):
#     print line
#
# line = 'spam'
# sing(line)

# Decorator with argument

def spam(repeats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(repeats):
                func(*args, **kwargs)
        return wrapper
    return decorator

@spam(5)
def sing(line):
    print line

line = 'spam'
sing(line)