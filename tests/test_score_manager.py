from src.managers.score_manager import ScoreManager


def test_save_and_load():
    sm = ScoreManager()
    sm.reset()
    sm.save_score(100, "easy")
    sm.save_score(200, "easy")
    top = sm.get_top_scores("easy")
    assert len(top) == 2
    assert top[0] == 200


def test_new_high_score():
    sm = ScoreManager()
    sm.reset()
    assert sm.is_new_high_score(50, "easy") is True
    sm.save_score(100, "easy")
    assert sm.is_new_high_score(50, "easy") is False
    assert sm.is_new_high_score(150, "easy") is True


def test_get_highest_score_empty():
    sm = ScoreManager()
    sm.reset()
    assert sm.get_highest_score("nonexistent") == 0


def test_top_scores_limit():
    sm = ScoreManager()
    sm.reset()
    for i in range(20):
        sm.save_score(i * 10, "hard")
    top = sm.get_top_scores("hard", 5)
    assert len(top) == 5
    assert top[0] == 190


def test_multiple_difficulties_independent():
    sm = ScoreManager()
    sm.reset()
    sm.save_score(100, "easy")
    sm.save_score(200, "hard")
    assert sm.get_highest_score("easy") == 100
    assert sm.get_highest_score("hard") == 200
