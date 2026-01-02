import httpx
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Footer, Header, ListItem, ListView, Static
from textual.containers import Vertical, Container

# Substitua pela sua chave da RAWG
API_KEY = "8f77617bd3d1480f914b5c6217753fad"

class GameEntry(ListItem):
    """Um item customizado na lista de resultados."""
    def __init__(self, title: str, rating: float):
        super().__init__()
        self.title = title
        self.rating = rating

    def compose(self) -> ComposeResult:
        yield Label(f"{self.title}  -  ⭐ {self.rating}")

class GameSearchApp(App):
    CSS_PATH = "search_games.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main-container"):
            yield Label("Busque um game")
            yield Input(placeholder="Digite o nome do jogo e aperte Enter...", id="search-input")
            
            with Container(id="results-container"):
                yield ListView(id="results-list")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if not query:
            return

        # Busca na API RAWG
        url = f"https://api.rawg.io/api/games?key={API_KEY}&search={query}&page_size=5"
        
        async with httpx.AsyncClient() as client:
            self.notify("Buscando...")
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                games = data.get("results", [])
                
                # Limpa e popula a lista
                results_list = self.query_one("#results-list", ListView)
                results_list.clear()
                
                for game in games:
                    results_list.append(GameEntry(game["name"], game.get("rating", 0)))
                
                # Mostra o container de resultados
                self.query_one("#results-container").add_class("has-results")
            else:
                self.notify("Erro na busca", severity="error")

if __name__ == "__main__":
    GameSearchApp().run()