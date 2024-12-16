from stockfish import Stockfish
import platform

system = platform.system()

if system == "Darwin":
    stockfish_path = "./stockfish"
elif system == "Windows":
    stockfish_path = "./stockfish-windows.exe"
else:
    pass

stockfish = Stockfish(stockfish_path)
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

best_move = stockfish.get_best_move()
print(f"Best move: {best_move}")