import subprocess

# Ruta a los archivos Python que deseas ejecutar
file1 = '42coin_node1.py'
file2 = '42coin_node2.py'
file3 = '42coin_node3.py'
# file4 = 'exec.py'

# Ejecutar los archivos Python en procesos separados
process1 = subprocess.Popen(['python', file1])
process2 = subprocess.Popen(['python', file2])
process3 = subprocess.Popen(['python', file3])
# process4 = subprocess.Popen(['python', file4])
# Esperar a que los procesos finalicen
process1.wait()
process2.wait()
process3.wait()
# process4.wait()
# Imprimir los códigos de salida de los procesos
print('Proceso 1 terminado con código de salida:', process1.returncode)
print('Proceso 2 terminado con código de salida:', process2.returncode)
print('Proceso 3 terminado con código de salida:', process3.returncode)
# print('Proceso 4 terminado con código de salida:', process4.returncode)
