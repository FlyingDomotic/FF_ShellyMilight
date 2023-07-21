Import("env")

progName = "not_found"
my_flags = env.ParseFlags(env['BUILD_FLAGS'])
#print(my_flags.get("CPPDEFINES"))
for x in my_flags.get("CPPDEFINES"):
    #print(x)
    if isinstance(x, list):
        k, v = x
        if k == "PROG_NAME":
            progName = v
            break

env.Replace(PROGNAME="%s" % str(progName))