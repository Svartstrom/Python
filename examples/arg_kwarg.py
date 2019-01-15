
def func(rec_arg, *args, **kwargs):
    print(rec_arg)

    if args:
        print(args)

    if kwargs:
        print(kwargs)

func("rec_arg",1,2,3,k1=4,k2="foo")
