"""Game state management: status, turns, move history, cursor/selection state."""

from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from board import Board, Move, UndoInfo
from pieces import Color, Piece, PieceType
from moves import get_legal_moves, is_in_check, is_checkmate, is_stalemate, move_to_algebraic
from ai import find_best_move


class GameStatus(Enum):
    """Current game status."""
    PLAYING = auto()
    CHECK = auto()
    CHECKMATE = auto()
    STALEMATE = auto()
    DRAW_50_MOVE = auto()
    DRAW_REPETITION = auto()
    RESIGNED = auto()


class InputMode(Enum):
    """Current input mode for the human player."""
    IDLE = auto()
    PIECE_SELECTED = auto()
    PROMOTING = auto()
    AI_THINKING = auto()
    GAME_OVER = auto()


class GameState:
    """Full game state including UI state."""

    def __init__(self) -> None:
        """Initialize a new game."""
        self.board = Board()
        self.status = GameStatus.PLAYING
        self.input_mode = InputMode.IDLE
        self.cursor_pos: Tuple[int, int] = (6, 4)  # Start on e2
        self.selected_square: Optional[Tuple[int, int]] = None
        self.legal_moves: List[Move] = []
        self.selected_piece_moves: List[Move] = []
        self.message: str = "White to move"
        self.move_history_text: List[str] = []
        self.captured_white: List[Piece] = []  # White pieces captured by black
        self.captured_black: List[Piece] = []  # Black pieces captured by white
        self.last_move: Optional[Move] = None
        self.position_history: Dict[str, int] = {}
        self.undo_stack: List[Tuple[Move, UndoInfo, str]] = []  # (move, undo, notation)
        self._update_legal_moves()
        self._record_position()

    def _update_legal_moves(self) -> None:
        """Refresh the cached legal moves for the current player."""
        self.legal_moves = get_legal_moves(self.board, self.board.turn)

    def _record_position(self) -> None:
        """Record the current position for repetition detection."""
        key = self.board.get_position_key()
        self.position_history[key] = self.position_history.get(key, 0) + 1

    def select_square(self, row: int, col: int) -> Optional[Move]:
        """Handle selection of a square. Returns the executed move if one was made."""
        if self.input_mode == InputMode.IDLE:
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.board.turn:
                moves = [m for m in self.legal_moves if m.from_sq == (row, col)]
                if moves:
                    self.selected_square = (row, col)
                    self.selected_piece_moves = moves
                    self.input_mode = InputMode.PIECE_SELECTED
            return None

        elif self.input_mode == InputMode.PIECE_SELECTED:
            # Check if clicking on another own piece
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.board.turn and (row, col) != self.selected_square:
                moves = [m for m in self.legal_moves if m.from_sq == (row, col)]
                if moves:
                    self.selected_square = (row, col)
                    self.selected_piece_moves = moves
                    return None

            # Check if this is a legal target
            matching = [m for m in self.selected_piece_moves if m.to_sq == (row, col)]
            if matching:
                if len(matching) > 1:
                    # Multiple moves to same square = promotion
                    self.input_mode = InputMode.PROMOTING
                    self._promotion_moves = matching
                    self.message = "Promote: Q/R/B/N"
                    return None
                else:
                    return self._execute_and_switch(matching[0])
            else:
                self.cancel_selection()
            return None
        return None

    def promote(self, piece_type: PieceType) -> Optional[Move]:
        """Complete a promotion by choosing the piece type."""
        if self.input_mode != InputMode.PROMOTING:
            return None
        for m in self._promotion_moves:
            if m.promotion == piece_type:
                return self._execute_and_switch(m)
        return None

    def _execute_and_switch(self, move: Move) -> Move:
        """Execute a move, record notation, update state."""
        notation = move_to_algebraic(self.board, move)
        undo = self.board.make_move(move)

        # Track captures
        if undo.captured_piece:
            if undo.captured_piece.color == Color.WHITE:
                self.captured_white.append(undo.captured_piece)
            else:
                self.captured_black.append(undo.captured_piece)

        self.undo_stack.append((move, undo, notation))
        self.last_move = move
        self.selected_square = None
        self.selected_piece_moves = []
        self.input_mode = InputMode.IDLE

        # Add to move history text
        move_num = (len(self.undo_stack) + 1) // 2
        if self.board.turn == Color.BLACK:
            # White just moved
            self.move_history_text.append(f"{move_num}. {notation}")
        else:
            # Black just moved
            if self.move_history_text:
                self.move_history_text[-1] += f"  {notation}"

        self._record_position()
        self._update_legal_moves()
        self.update_status()
        return move

    def cancel_selection(self) -> None:
        """Cancel current piece selection."""
        self.selected_square = None
        self.selected_piece_moves = []
        if self.input_mode == InputMode.PIECE_SELECTED or self.input_mode == InputMode.PROMOTING:
            self.input_mode = InputMode.IDLE

    def execute_ai_move(self) -> Optional[Move]:
        """Have the AI compute and execute a move."""
        self.input_mode = InputMode.AI_THINKING
        self.message = "Computer thinking..."
        move = find_best_move(self.board, Color.BLACK, depth=3)
        if move:
            return self._execute_and_switch(move)
        self.input_mode = InputMode.IDLE
        self.update_status()
        return None

    def undo_last_move(self) -> None:
        """Undo the last full move pair (AI + human)."""
        # Undo AI move
        if self.undo_stack and self.board.turn == Color.WHITE:
            move, undo, _ = self.undo_stack.pop()
            if undo.captured_piece:
                if undo.captured_piece.color == Color.WHITE:
                    if self.captured_white:
                        self.captured_white.pop()
                else:
                    if self.captured_black:
                        self.captured_black.pop()
            self.board.unmake_move(move, undo)
            if self.move_history_text:
                # Remove black's part from last entry
                last = self.move_history_text[-1]
                if '  ' in last:
                    self.move_history_text[-1] = last.rsplit('  ', 1)[0]
                else:
                    self.move_history_text.pop()

        # Undo human move
        if self.undo_stack and self.board.turn == Color.BLACK:
            move, undo, _ = self.undo_stack.pop()
            if undo.captured_piece:
                if undo.captured_piece.color == Color.WHITE:
                    if self.captured_white:
                        self.captured_white.pop()
                else:
                    if self.captured_black:
                        self.captured_black.pop()
            self.board.unmake_move(move, undo)
            if self.move_history_text:
                self.move_history_text.pop()

        self.last_move = self.undo_stack[-1][0] if self.undo_stack else None
        self.selected_square = None
        self.selected_piece_moves = []
        self.input_mode = InputMode.IDLE
        self.status = GameStatus.PLAYING
        self._update_legal_moves()
        self.update_status()

    def new_game(self) -> None:
        """Reset to a new game."""
        self.__init__()

    def update_status(self) -> None:
        """Update game status (check, checkmate, stalemate, draws)."""
        color = self.board.turn

        if is_checkmate(self.board, color):
            self.status = GameStatus.CHECKMATE
            winner = "White" if color == Color.BLACK else "Black"
            self.message = f"Checkmate! {winner} wins!"
            self.input_mode = InputMode.GAME_OVER
        elif is_stalemate(self.board, color):
            self.status = GameStatus.STALEMATE
            self.message = "Stalemate! Draw."
            self.input_mode = InputMode.GAME_OVER
        elif self.board.halfmove_clock >= 100:
            self.status = GameStatus.DRAW_50_MOVE
            self.message = "Draw by 50-move rule."
            self.input_mode = InputMode.GAME_OVER
        elif max(self.position_history.values(), default=0) >= 3:
            self.status = GameStatus.DRAW_REPETITION
            self.message = "Draw by repetition."
            self.input_mode = InputMode.GAME_OVER
        elif is_in_check(self.board, color):
            self.status = GameStatus.CHECK
            self.message = f"{'White' if color == Color.WHITE else 'Black'} is in check!"
        else:
            self.status = GameStatus.PLAYING
            turn_name = "White" if color == Color.WHITE else "Black"
            self.message = f"{turn_name} to move"
