from gamebot.games.tictactoe import TictactoeEngine, TictactoeState

def gen_state(board):
    return TictactoeState(None, 0, board)

def test_possible_next_states_empty_board():
    state = gen_state([[-1 for _ in range(3)] for _ in range(3)])
    generator = state.possible_next_states()

    expected = [i for i in range(9)]
    for state in generator:
        assert expected
        expected.remove(state.last_move)

    assert expected == []

def test_possible_next_states_full_board():
    state = gen_state([[0 for _ in range(3)] for _ in range(3)])
    generator = state.possible_next_states()

    for state in generator: # The generator should be empty
        assert False

    assert True

def test_possible_next_states_winner():
    state = gen_state([[0, 0, 0], [-1, -1, -1], [-1, -1,-1]])
    generator = state.possible_next_states()

    expected = [i for i in range(3, 9)]
    for state in generator:
        assert expected
        expected.remove(state.last_move)

    assert expected == []

def test_possible_next_states_random():
    state = gen_state([[0, -1, 0], [-1, 1, -1], [0, 1,-1]])
    generator = state.possible_next_states()

    expected = [1, 3, 5, 8]
    for state in generator:
        assert expected
        expected.remove(state.last_move)

    assert expected == []

def test_is_tie():
    state = gen_state([[0, 1, 0], [1, 0, 1], [1, 0,1]])
    assert state.is_tie()

def test_is_not_tie_winner():
    state = gen_state([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert not state.is_tie()

def test_is_not_tie_not_finish():
    state = gen_state([[0, 1, -1], [1, 0, 1], [-1, 1, -1]])
    assert not state.is_tie()

def test_is_not_tie_empty():
    state = gen_state([[-1 for _ in range(3)] for _ in range(3)])
    assert not state.is_tie()

def test_has_won_0_diag1():
    state = gen_state([[0, -1, -1], [-1, 0, -1], [-1, -1, 0]])
    assert state.has_won(0)

def test_has_won_1_diag2():
    state = gen_state([[-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    assert state.has_won(1)

def test_has_not_won_0_diag2():
    state = gen_state([[-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    assert not state.has_won(0)

def test_has_won_0_row1():
    state = gen_state([[0, 0, 0], [1, 1, 0], [1, -1, -1]])
    assert state.has_won(0)

def test_has_won_0_row2():
    state = gen_state([[1, 0, 0], [0, 0, 0], [1, -1, -1]])
    assert state.has_won(0)

def test_has_won_0_row3():
    state = gen_state([[1, 0,-1], [0, 1, 0], [0, 0, 0]])
    assert state.has_won(0)

def test_has_won_1_col1():
    state = gen_state([[1, 0,-1], [1, 1, 0], [1, 0, 0]])
    assert state.has_won(1)

def test_has_not_won_1():
    state = gen_state([[1, 0, 1], [0,-1, 0], [1, -1, 1]])
    assert not state.has_won(1)

def test_next_player_0():
    state = TictactoeState(None, 0, None)
    assert state.next_player == 1

def test_next_player_1():
    state = TictactoeState(None, 1, None)
    assert state.next_player == 0
