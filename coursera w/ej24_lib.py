print('Let\'s practice everything')
print('You\'d need to know \'about escapes with \\ that do :')
print('\n newlines and \t tabs.')

poem = """
\tThe lovely world with logic so firmly planted cannot discern  \n the needs of love nor comprehend passion from intuiton and requieres ab esxplanation \n\t\twhere there si one.
"""
print('-----------')
print(poem)
print('-----------')


five = 10 - 2 + 3 - 6
print(f'This should be {five}')


def secret_formula(started):
    jelly_beans = started * 500
    jars = jelly_beans / 1000
    crates = jars / 100
    return jelly_beans, jars, crates

