# def greet(name):
#     return "Hello " + name
#
# def call_func(func):
#     other_name = "John"
#     return func(other_name)
#
# print(call_func(greet))

# Outputs: Hello John

def call_func(func):
    def wrap(*args,**kwargs):
        other_name = "John"
        if args:
            return func(*args)
        return func(other_name)
    return wrap

def repeat(n):
    
@call_func
def greet(name):
    return "Hello "+name

print(greet())
print(greet("J"))
