import tkinter as tk
from tkinter import ttk, messagebox
from package.produtos import Roupa, Eletronico, Alimento
from package.carrinho_pkg import Carrinho
from package.caixa_pkg import Caixa
import banco

# ── Cores e estilos ──────────────────────────────────────────────────────────
BG        = "#1a1a2e"
BG2       = "#16213e"
ACCENT    = "#0f3460"
BTN       = "#e94560"
BTN_HOVER = "#c73652"
TEXT      = "#eaeaea"
TEXT2     = "#a0a0b0"
GREEN     = "#4ecca3"
WHITE     = "#ffffff"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_SUB    = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)

banco.criar_tabelas()
carrinho = Carrinho()
for p in banco.carregar_objetos():
    carrinho._produtos.append(p)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Loja de Produtos")
        self.geometry("860x580")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build()

    def _build(self):
        # Sidebar
        side = tk.Frame(self, bg=ACCENT, width=200)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="🛍️  Loja", font=FONT_TITLE,
                 bg=ACCENT, fg=WHITE).pack(pady=(28, 6))
        tk.Label(side, text="Sistema de Produtos", font=FONT_SMALL,
                 bg=ACCENT, fg=TEXT2).pack(pady=(0, 30))

        self.frames = {}
        pages = [
            ("Produtos",  PaginaProdutos),
            ("Carrinho",  PaginaCarrinho),
            ("Caixa",     PaginaCaixa),
        ]

        for name, cls in pages:
            frame = cls(self.container(), self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            btn = tk.Button(side, text=name, font=FONT_SUB,
                            bg=ACCENT, fg=WHITE, relief="flat",
                            activebackground=BTN, activeforeground=WHITE,
                            cursor="hand2", pady=12,
                            command=lambda n=name: self.show(n))
            btn.pack(fill="x", padx=10, pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=ACCENT))

        self.show("Produtos")

    def container(self):
        if not hasattr(self, "_container"):
            self._container = tk.Frame(self, bg=BG)
            self._container.pack(side="right", fill="both", expand=True)
            self._container.grid_rowconfigure(0, weight=1)
            self._container.grid_columnconfigure(0, weight=1)
        return self._container

    def show(self, name):
        frame = self.frames[name]
        if hasattr(frame, "atualizar"):
            frame.atualizar()
        frame.tkraise()


# ── Helpers de UI ─────────────────────────────────────────────────────────────

def label(parent, text, font=FONT_BODY, fg=TEXT, bg=BG, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def entry(parent, **kw):
    e = tk.Entry(parent, font=FONT_BODY, bg=BG2, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=ACCENT,
                 highlightcolor=BTN, **kw)
    return e


def btn(parent, text, cmd, color=BTN, **kw):
    b = tk.Button(parent, text=text, command=cmd, font=FONT_SUB,
                  bg=color, fg=WHITE, relief="flat", cursor="hand2",
                  activebackground=BTN_HOVER, activeforeground=WHITE,
                  padx=14, pady=7, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=BTN_HOVER))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b


def section_title(parent, text):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", padx=24, pady=(20, 4))
    label(f, text, font=FONT_TITLE, fg=GREEN).pack(side="left")
    tk.Frame(f, bg=ACCENT, height=2).pack(side="left", fill="x",
                                           expand=True, padx=(12, 0), pady=8)


# ── Página Produtos ───────────────────────────────────────────────────────────

class PaginaProdutos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        section_title(self, "Adicionar Produto")

        # Tipo
        tipo_frame = tk.Frame(self, bg=BG)
        tipo_frame.pack(fill="x", padx=24, pady=(0, 12))
        label(tipo_frame, "Tipo:").pack(side="left", padx=(0, 10))
        self.tipo_var = tk.StringVar(value="Roupa")
        for t in ["Roupa", "Eletronico", "Alimento"]:
            rb = tk.Radiobutton(tipo_frame, text=t, variable=self.tipo_var,
                                value=t, font=FONT_BODY, bg=BG, fg=TEXT,
                                selectcolor=ACCENT, activebackground=BG,
                                activeforeground=GREEN, command=self._toggle)
            rb.pack(side="left", padx=8)

        # Campos
        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=24)

        label(form, "Nome:").grid(row=0, column=0, sticky="w", pady=5)
        self.e_nome = entry(form, width=28)
        self.e_nome.grid(row=0, column=1, pady=5, padx=(8, 0))

        label(form, "Preço (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.e_preco = entry(form, width=28)
        self.e_preco.grid(row=1, column=1, pady=5, padx=(8, 0))

        self.lbl_extra = label(form, "Tamanho:")
        self.lbl_extra.grid(row=2, column=0, sticky="w", pady=5)
        self.e_extra = entry(form, width=28)
        self.e_extra.grid(row=2, column=1, pady=5, padx=(8, 0))

        btn(self, "  + Adicionar ao Carrinho", self._adicionar).pack(
            anchor="w", padx=24, pady=14)

        # Lista
        section_title(self, "Produtos no Banco")
        self.tree = self._tabela(["Tipo", "Nome", "Preço", "Detalhe"])
        self.atualizar()

    def _tabela(self, cols):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG2, foreground=TEXT,
                        fieldbackground=BG2, font=FONT_BODY, rowheight=26)
        style.configure("Treeview.Heading", background=ACCENT,
                        foreground=WHITE, font=FONT_SUB)
        style.map("Treeview", background=[("selected", BTN)])
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=7)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140)
        tree.pack(fill="both", expand=True)
        return tree

    def _toggle(self):
        t = self.tipo_var.get()
        labels = {"Roupa": "Tamanho (P/M/G):",
                  "Eletronico": "Garantia (meses):",
                  "Alimento": "Validade (MM/AAAA):"}
        self.lbl_extra.config(text=labels[t])

    def _adicionar(self):
        nome  = self.e_nome.get().strip()
        preco = self.e_preco.get().strip()
        extra = self.e_extra.get().strip()
        if not nome or not preco or not extra:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        try:
            preco = float(preco)
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido.")
            return
        tipo = self.tipo_var.get()
        if tipo == "Roupa":
            p = Roupa(nome, preco, extra)
        elif tipo == "Eletronico":
            p = Eletronico(nome, preco, int(extra))
        else:
            p = Alimento(nome, preco, extra)
        carrinho.adicionar(p)
        banco.salvar_objeto(p)
        self.e_nome.delete(0, "end")
        self.e_preco.delete(0, "end")
        self.e_extra.delete(0, "end")
        self.atualizar()
        messagebox.showinfo("✅", f"'{nome}' adicionado ao carrinho!")

    def atualizar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in banco.carregar_objetos():
            tipo = type(p).__name__
            if hasattr(p, "tamanho"):   extra = p.tamanho
            elif hasattr(p, "garantia"): extra = f"{p.garantia} meses"
            else:                        extra = p.validade
            self.tree.insert("", "end",
                             values=(tipo, p.nome, f"R$ {p.preco:.2f}", extra))


# ── Página Carrinho ───────────────────────────────────────────────────────────

class PaginaCarrinho(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        section_title(self, "Carrinho")

        style = ttk.Style()
        style.configure("Treeview", background=BG2, foreground=TEXT,
                        fieldbackground=BG2, font=FONT_BODY, rowheight=26)
        style.configure("Treeview.Heading", background=ACCENT,
                        foreground=WHITE, font=FONT_SUB)
        style.map("Treeview", background=[("selected", BTN)])

        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=24)
        cols = ["Tipo", "Nome", "Preço", "Detalhe"]
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.pack(fill="both", expand=True)

        # Total
        self.lbl_total = label(self, "Total: R$ 0.00",
                               font=("Segoe UI", 13, "bold"), fg=GREEN)
        self.lbl_total.pack(anchor="e", padx=28, pady=8)

        # Botão remover
        btn(self, "  🗑  Remover Selecionado", self._remover,
            color="#444").pack(anchor="w", padx=24, pady=(0, 6))

        self.atualizar()

    def _remover(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um item.")
            return
        nome = self.tree.item(sel[0])["values"][1]
        carrinho.remover(nome)
        banco.remover_objeto(nome)
        self.atualizar()

    def atualizar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in carrinho.produtos:
            tipo = type(p).__name__
            if hasattr(p, "tamanho"):    extra = p.tamanho
            elif hasattr(p, "garantia"): extra = f"{p.garantia} meses"
            else:                        extra = p.validade
            self.tree.insert("", "end",
                             values=(tipo, p.nome, f"R$ {p.preco:.2f}", extra))
        self.lbl_total.config(text=f"Total: R$ {carrinho.total():.2f}")


# ── Página Caixa ──────────────────────────────────────────────────────────────

class PaginaCaixa(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        section_title(self, "Caixa")

        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=24, pady=(8, 0))
        label(form, "Operador:").grid(row=0, column=0, sticky="w", pady=6)
        self.e_op = entry(form, width=28)
        self.e_op.grid(row=0, column=1, padx=(8, 0))

        btn(self, "  ✅  Finalizar Compra", self._finalizar).pack(
            anchor="w", padx=24, pady=14)

        section_title(self, "Histórico de Compras")

        style = ttk.Style()
        style.configure("Treeview", background=BG2, foreground=TEXT,
                        fieldbackground=BG2, font=FONT_BODY, rowheight=26)
        style.configure("Treeview.Heading", background=ACCENT,
                        foreground=WHITE, font=FONT_SUB)
        style.map("Treeview", background=[("selected", BTN)])

        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        cols = ["#", "Data", "Operador", "Total"]
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        widths = [40, 160, 160, 100]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)
        self.tree.pack(fill="both", expand=True)
        self.atualizar()

    def _finalizar(self):
        operador = self.e_op.get().strip()
        if not operador:
            messagebox.showwarning("Atenção", "Informe o nome do operador.")
            return
        if not carrinho.produtos:
            messagebox.showwarning("Atenção", "Carrinho vazio.")
            return
        total = carrinho.total()
        banco.registrar_compra(operador, total)
        banco.limpar_carrinho()
        carrinho._produtos.clear()
        self.e_op.delete(0, "end")
        self.atualizar()
        self.app.frames["Carrinho"].atualizar()
        self.app.frames["Produtos"].atualizar()
        messagebox.showinfo("✅ Compra Finalizada",
                            f"Total: R$ {total:.2f}\nOperador: {operador}")

    def atualizar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, (id, op, total, data) in enumerate(banco.listar_compras(), 1):
            self.tree.insert("", "end",
                             values=(i, data, op, f"R$ {total:.2f}"))


if __name__ == "__main__":
    App().mainloop()
