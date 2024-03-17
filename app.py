import sqlite3

class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

class TaskList:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, description TEXT, completed INTEGER)')
        self.conn.commit()

    def add_task(self, description):
        self.cursor.execute('INSERT INTO tasks (description, completed) VALUES (?, ?)', (description, 0))
        self.conn.commit()

    def delete_task(self, id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
        self.conn.commit()

    def toggle_task_completion(self, id):
        self.cursor.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?', (id,))
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Task(row[0], row[1], row[2]))
        return tasks

task_list = TaskList()

def print_tasks():
    tasks = task_list.get_tasks()
    for task in tasks:
        print(f"{task.id}. [{'X' if task.completed else ' '}] {task.description}")

while True:
    print("\nLista de Tarefas:")
    print_tasks()
    print("\nOpções:")
    print("1. Adicionar Tarefa")
    print("2. Excluir Tarefa")
    print("3. Marcar/Desmarcar Tarefa como Concluída")
    print("0. Sair")

    option = input("Escolha uma opção: ")

    if option == '1':
        description = input("Digite a descrição da nova tarefa: ")
        task_list.add_task(description)
    elif option == '2':
        id = int(input("Digite o número da tarefa a ser excluída: "))
        task_list.delete_task(id)
    elif option == '3':
        id = int(input("Digite o número da tarefa para marcar/desmarcar como concluída: "))
        task_list.toggle_task_completion(id)
    elif option == '0':
        print("Saindo do aplicativo...")
        break
    else:
        print("Opção inválida. Por favor, tente novamente.")

