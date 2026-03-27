"""AI engine: evaluation function and minimax search with alpha-beta pruning."""

from typing import List, Optional, Tuple

from board import Board, Move
from pieces import Color, Piece, PieceType, PIECE_VALUES, PIECE_SQUARE_TABLES
from moves import get_legal_moves, is_in_check

INF = 999999


def evaluate(board: Board) -> int:
    """Evaluate the board position. Positive = white advantage, negative = black advantage."""
    score = 0
    white_bishops = 0
    black_bishops = 0

    for r in range(8):
        for c in range(8):
            piece = board.get_piece(r, c)
            if piece is None:
                continue

            # Material value
            val = PIECE_VALUES[piece.piece_type]

            # Piece-square table bonus
            table = PIECE_SQUARE_TABLES[piece.piece_type]
            if piece.color == Color.WHITE:
                pst_bonus = table[r][c]
                score += val + pst_bonus
                if piece.piece_type == PieceType.BISHOP:
                    white_bishops += 1
            else:
                pst_bonus = table[7 - r][c]  # Mirror vertically for black
                score -= val + pst_bonus
                if piece.piece_type == PieceType.BISHOP:
                    black_bishops += 1

    # Bishop pair bonus
    if white_bishops >= 2:
        score += 50
    if black_bishops >= 2:
        score -= 50

    return score


def order_moves(board: Board, moves: List[Move]) -> List[Move]:
    """Order moves for better alpha-beta pruning (captures first, MVV-LVA)."""
    def move_score(move: Move) -> int:
        score = 0
        target = board.get_piece(move.to_sq[0], move.to_sq[1])
        if target:
            # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
            attacker = board.get_piece(move.from_sq[0], move.from_sq[1])
            score = 10 * PIECE_VALUES[target.piece_type]
            if attacker:
                score -= PIECE_VALUES[attacker.piece_type]
        if move.promotion:
            score += PIECE_VALUES[move.promotion]
        return score

    return sorted(moves, key=move_score, reverse=True)


def quiescence_search(board: Board, alpha: int, beta: int, maximizing: bool) -> int:
    """Search only capture sequences to avoid horizon effect."""
    stand_pat = evaluate(board)

    if maximizing:
        if stand_pat >= beta:
            return beta
        if stand_pat > alpha:
            alpha = stand_pat

        color = board.turn
        moves = get_legal_moves(board, color)
        captures = [m for m in moves if board.get_piece(m.to_sq[0], m.to_sq[1]) is not None
                    or m.is_en_passant]
        captures = order_moves(board, captures)

        for move in captures:
            undo = board.make_move(move)
            score = quiescence_search(board, alpha, beta, False)
            board.unmake_move(move, undo)
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break
        return alpha
    else:
        if stand_pat <= alpha:
            return alpha
        if stand_pat < beta:
            beta = stand_pat

        color = board.turn
        moves = get_legal_moves(board, color)
        captures = [m for m in moves if board.get_piece(m.to_sq[0], m.to_sq[1]) is not None
                    or m.is_en_passant]
        captures = order_moves(board, captures)

        for move in captures:
            undo = board.make_move(move)
            score = quiescence_search(board, alpha, beta, True)
            board.unmake_move(move, undo)
            if score < beta:
                beta = score
            if alpha >= beta:
                break
        return beta


def minimax(board: Board, depth: int, alpha: int, beta: int,
            maximizing: bool) -> Tuple[int, Optional[Move]]:
    """Minimax search with alpha-beta pruning."""
    color = board.turn
    moves = get_legal_moves(board, color)

    if len(moves) == 0:
        if is_in_check(board, color):
            # Checkmate - worse the deeper it is (prefer faster mate)
            return (-INF + (100 - depth) if maximizing else INF - (100 - depth)), None
        return 0, None  # Stalemate

    if depth == 0:
        return quiescence_search(board, alpha, beta, maximizing), None

    moves = order_moves(board, moves)
    best_move = moves[0]

    if maximizing:
        max_eval = -INF
        for move in moves:
            undo = board.make_move(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False)
            board.unmake_move(move, undo)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = INF
        for move in moves:
            undo = board.make_move(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True)
            board.unmake_move(move, undo)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def find_best_move(board: Board, color: Color, depth: int = 3) -> Optional[Move]:
    """Find the best move for the given color at the specified search depth."""
    moves = get_legal_moves(board, color)
    if not moves:
        return None

    maximizing = (color == Color.WHITE)
    _, best_move = minimax(board, depth, -INF, INF, maximizing)
    return best_move
