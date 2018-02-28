


def modulefunction():
    print("This is modulefunction running in samplemodule.py")


print("Code inside samplemodule")

if __name__ == '__main__':
    # This is the code running when you run this file directly
    print("Start of main run of samplemodule")
    modulefunction()
    print("End of samplemodule")