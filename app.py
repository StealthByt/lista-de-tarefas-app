import sqlite3
from colorama import Fore, Style, init
import os

# Inicializar colorama
init(autoreset=True)

# Função para criar uma conexão com o banco de dados
def create_connection(db_file):
    return sqlite3.connect(db_file)

# Função para criar a tabela de tarefas
def create_table(conn):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                done BOOLEAN NOT NULL CHECK (done IN (0, 1))
            );
        """)

# Função para adicionar uma tarefa
def add_task(conn, title, description):
    with conn:
        conn.execute("INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)", (title, description, 0))

# Função para excluir uma tarefa
def delete_task(conn, task_id):
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            print(Fore.RED + "[Erro] Tarefa não encontrada.")
        else:
            print(Fore.RED + "[Tarefa Excluída] ✔")

# Função para marcar/desmarcar uma tarefa como feita
def toggle_task_done(conn, task_id):
    cur = conn.cursor()
    cur.execute("SELECT done FROM tasks WHERE id = ?", (task_id,))
    result = cur.fetchone()
    
    if result is None:
        print(Fore.RED + "[Erro] Tarefa não encontrada.")
        return
    
    current_status = result[0]
    new_status = 0 if current_status else 1
    with conn:
        conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_status, task_id))
        print(Fore.GREEN + "[Tarefa Atualizada] ✔")

# Função para listar todas as tarefas
def list_tasks(conn):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar tela
    print(Fore.GREEN + "█████████████████████████████████████████████████████")
    print(Fore.GREEN + "█████████████████████████████████████████████████████")
    print(Fore.YELLOW + "          📋 Lista de Tarefas 📋")
    print(Fore.GREEN + "█████████████████████████████████████████████████████")
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, done FROM tasks ORDER BY id")
    tasks = cur.fetchall()
    if tasks:
        for index, task in enumerate(tasks, start=1):
            id, title, description, done = task
            done_status = Fore.GREEN + "[✔]" if done else Fore.RED + "[ ]"
            print(f"{Fore.CYAN}{index:>3}. {done_status} {Fore.WHITE}{title:<30} {description}")
    else:
        print(Fore.RED + "Nenhuma tarefa encontrada.")
    print(Fore.GREEN + "█████████████████████████████████████████████████████")

# Função para exibir o menu
def menu():
    print(Fore.YELLOW + "\nOpções:")
    print(Fore.YELLOW + "1. Adicionar Tarefa")
    print(Fore.YELLOW + "2. Excluir Tarefa")
    print(Fore.YELLOW + "3. Marcar/Desmarcar Tarefa como Concluída")
    print(Fore.YELLOW + "0. Sair")
    choice = input(Fore.CYAN + "Escolha uma opção: ")
    return choice

# Função principal
def main():
    database = 'tasks.db'
    conn = create_connection(database)
    create_table(conn)

    while True:
        list_tasks(conn)
        choice = menu()

        if choice == '1':
            title = input(Fore.CYAN + "Título da tarefa: ")
            description = input(Fore.CYAN + "Descrição da tarefa (ex.: 1hr, 30min): ")
            add_task(conn, title, description)
            print(Fore.GREEN + "[Tarefa Adicionada] ✔")
        elif choice == '2':
            task_index = int(input(Fore.CYAN + "Número da tarefa a ser excluída: ")) - 1
            task_id = get_task_id_by_index(conn, task_index)
            if task_id is not None:
                delete_task(conn, task_id)
            else:
                print(Fore.RED + "[Erro] Número da tarefa inválido.")
        elif choice == '3':
            task_index = int(input(Fore.CYAN + "Número da tarefa para marcar/desmarcar como concluída: ")) - 1
            task_id = get_task_id_by_index(conn, task_index)
            if task_id is not None:
                toggle_task_done(conn, task_id)
            else:
                print(Fore.RED + "[Erro] Número da tarefa inválido.")
        elif choice == '0':
            print(Fore.GREEN + "Saindo do programa... Até logo! 👋")
            break
        else:
            print(Fore.RED + "[Opção Inválida] ❌ Tente novamente.")

    conn.close()

# Função para obter o ID da tarefa a partir do índice exibido
def get_task_id_by_index(conn, index):
    cur = conn.cursor()
    cur.execute("SELECT id FROM tasks ORDER BY id")
    ids = [row[0] for row in cur.fetchall()]
    if 0 <= index < len(ids):
        return ids[index]
    return None

if __name__ == '__main__':
    main()
