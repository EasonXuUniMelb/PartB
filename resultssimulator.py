import subprocess
import sys

command1 = 'python -m referee agent agent-random'
command2 = 'python -m referee agent-minimax2 agent'
command3 = 'python -m referee agent-minimax2 agent-random'
command4 = 'python -m referee agent-random agent'
command5 = 'python -m referee agent agent-minimax2'
command6 = 'python -m referee agent-random agent-minimax2'
output_prefix1 = 'output minimaxab vs random'
output_prefix2 = 'output minimax vs minimaxab'
output_prefix3 = 'output minimax vs random'
output_prefix4 = 'output random vs minimaxab'
output_prefix5 = 'output minimaxab vs minimax'
output_prefix6 = 'output random vs minimax'

n_iter = 20
for i in range(n_iter):
    output_file = output_prefix1 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command1, stdout=sys.stdout, stderr=subprocess.STDOUT)
    
for i in range(n_iter):
    output_file = output_prefix2 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command2, stdout=sys.stdout, stderr=subprocess.STDOUT)

for i in range(n_iter):
    output_file = output_prefix3 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command3, stdout=sys.stdout, stderr=subprocess.STDOUT)
    
for i in range(n_iter):
    output_file = output_prefix4 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command4, stdout=sys.stdout, stderr=subprocess.STDOUT)
    
for i in range(n_iter):
    output_file = output_prefix5 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command5, stdout=sys.stdout, stderr=subprocess.STDOUT)

for i in range(n_iter):
    output_file = output_prefix6 + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(command6, stdout=sys.stdout, stderr=subprocess.STDOUT)