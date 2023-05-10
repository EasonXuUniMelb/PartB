import subprocess
import sys

command1 = 'python -m referee agent-random agent-minimax2 '
output_prefix1 = 'test'

n_iter = 10
for i in range(n_iter):
    output_file = output_prefix1 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command1, stdout=sys.stdout, stderr=subprocess.STDOUT)