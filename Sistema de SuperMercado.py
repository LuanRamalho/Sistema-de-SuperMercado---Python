import tkinter as tk
from tkinter import messagebox

# Inicializando a lista de produtos e o preço total
products = []
totalPrice = 0.0

# Função para adicionar um produto
def add_product():
    code = product_code_entry.get()
    name = product_name_entry.get()
    try:
        quantity = float(product_quantity_entry.get())
        price = float(product_price_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para quantidade e preço.")
        return

    if code and name and quantity and price:
        product = {
            "code": code,
            "name": name,
            "quantity": quantity,
            "price": price,
            "subTotal": quantity * price
        }
        products.append(product)
        update_product_list()
        update_total_price()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

# Função para remover um produto
def remove_product():
    code = product_code_entry.get()
    global products
    products = [p for p in products if p["code"] != code]
    update_product_list()
    update_total_price()

# Função para atualizar a lista de produtos na interface
def update_product_list():
    product_list.delete(0, tk.END)
    for product in products:
        product_text = (
            f"Código: {product['code']} | "
            f"Nome: {product['name']} | "
            f"Quantidade/Peso: {product['quantity']} | "
            f"Preço: R$ {product['price']:.2f} | "
            f"Sub-total: R$ {product['subTotal']:.2f}"
        )
        product_list.insert(tk.END, product_text)

# Função para selecionar um produto da lista e preencher os campos de entrada
def select_product(event):
    selected_product = product_list.get(product_list.curselection())
    selected_code = selected_product.split(" | ")[0].split(": ")[1]
    for product in products:
        if product["code"] == selected_code:
            product_code_entry.delete(0, tk.END)
            product_code_entry.insert(tk.END, product["code"])
            product_name_entry.delete(0, tk.END)
            product_name_entry.insert(tk.END, product["name"])
            product_quantity_entry.delete(0, tk.END)
            product_quantity_entry.insert(tk.END, product["quantity"])
            product_price_entry.delete(0, tk.END)
            product_price_entry.insert(tk.END, product["price"])
            break

# Função para atualizar o preço total
def update_total_price():
    global totalPrice
    totalPrice = sum(p["subTotal"] for p in products)
    total_price_label.config(text=f"Total: R$ {totalPrice:.2f}")
    calculate_change()

# Função para calcular o troco
def calculate_change():
    try:
        amount_paid = float(amount_paid_entry.get())
        change = amount_paid - totalPrice
        change_label.config(text=f"Troco: R$ {change:.2f}" if change >= 0 else "Troco: R$ 0.00")
    except ValueError:
        change_label.config(text="Troco: R$ 0.00")

# Configurações da janela principal
root = tk.Tk()
root.title("Simulação de Supermercado")
root.geometry("700x600")
root.configure(bg="#f0f8ff")

# Título principal
title_label = tk.Label(root, text="Simulação de Supermercado", font=("Arial", 28, "bold"), bg="#4682b4", fg="white", pady=10)
title_label.pack(fill=tk.X)

# Seção de entrada de produtos
product_frame = tk.Frame(root, bg="#f0f8ff")
product_frame.pack(pady=10)

product_code_label = tk.Label(product_frame, text="Código do Produto:", bg="#f0f8ff", font=("Arial", 12))
product_code_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
product_code_entry = tk.Entry(product_frame, width=25)
product_code_entry.grid(row=0, column=1, padx=10, pady=5)

product_name_label = tk.Label(product_frame, text="Nome do Produto:", bg="#f0f8ff", font=("Arial", 12))
product_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
product_name_entry = tk.Entry(product_frame, width=25)
product_name_entry.grid(row=1, column=1, padx=10, pady=5)

product_quantity_label = tk.Label(product_frame, text="Quantidade/Peso:", bg="#f0f8ff", font=("Arial", 12))
product_quantity_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
product_quantity_entry = tk.Entry(product_frame, width=25)
product_quantity_entry.grid(row=2, column=1, padx=10, pady=5)

product_price_label = tk.Label(product_frame, text="Preço:", bg="#f0f8ff", font=("Arial", 12))
product_price_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
product_price_entry = tk.Entry(product_frame, width=25)
product_price_entry.grid(row=3, column=1, padx=10, pady=5)

# Botões de ação
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Adicionar Produto", command=add_product, bg="#32cd32", fg="white", font=("Arial", 12, "bold"), width=15)
add_button.grid(row=0, column=0, padx=5, pady=5)

remove_button = tk.Button(button_frame, text="Excluir Produto", command=remove_product, bg="#dc143c", fg="white", font=("Arial", 12, "bold"), width=15)
remove_button.grid(row=0, column=1, padx=5, pady=5)

# Lista de produtos
product_list_label = tk.Label(root, text="Lista de Produtos", bg="#4682b4", fg="white", font=("Arial", 16, "bold"))
product_list_label.pack(pady=10, fill=tk.X)
product_list = tk.Listbox(root, height=10, width=60, font=("Arial", 10))
product_list.pack()
product_list.bind("<<ListboxSelect>>", select_product)

# Exibição do preço total
total_price_label = tk.Label(root, text="Total: R$ 0.00", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2e8b57")
total_price_label.pack(pady=10)

# Campo de entrada e exibição do troco
amount_paid_label = tk.Label(root, text="Valor Pago:", bg="#f0f8ff", font=("Arial", 12))
amount_paid_label.pack()
amount_paid_entry = tk.Entry(root, width=20)
amount_paid_entry.pack()
amount_paid_entry.bind("<KeyRelease>", lambda event: calculate_change())

change_label = tk.Label(root, text="Troco: R$ 0.00", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2e8b57")
change_label.pack(pady=10)

# Executar a interface gráfica
root.mainloop()
