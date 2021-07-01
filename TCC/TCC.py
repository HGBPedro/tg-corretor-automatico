import io
import language_tool_python
from nltk import text

#tool = language_tool_python.LanguageTool('pt-PT')
tool = language_tool_python.LanguageTool('pt-BR')
testeCorrecao = input('Insira o caminho do arquivo: ')

#file = open('E:\\TCC\\teste.txt', 'r')
file = open(testeCorrecao, 'r')

text = file.read()

print(text)

corrigido = tool.check(text)

#writer = open('E:\\TCC\\teste.txt', 'a')
writer = open(testeCorrecao, 'a')
writer.write('\n\nCorreções:\n\n')

if len(corrigido) > 0:
    for item in corrigido:
        writer.write(str(item))
        writer.write('\n\n')

print(corrigido)
