from app.rewards import (
    affordable_items,
    evaluate_gate,
    proofread_points,
    scene_reward,
)


def test_scene_reward_bonus():
    assert scene_reward("fall-01", "s1", all_green=False).points == 10
    assert scene_reward("fall-01", "s1", all_green=True).points == 15
    assert scene_reward("fall-01", "s1", False).panel_key == "panel:fall-01:s1"


def test_proofread_points_with_perfect_bonus():
    assert proofread_points(0, 4) == 0
    assert proofread_points(2, 4) == 10
    assert proofread_points(4, 4) == 30   # 4*5 + 10 Bonus


def test_affordable_items_scale_with_points():
    assert affordable_items(0) == []
    assert "lupe" in affordable_items(20)
    assert "mantel" in affordable_items(50)


def test_gate_uncalibrated_always_continues():
    g = evaluate_gate(None, calibrated=False, min_advance=0.55, green=0.8, all_green=False)
    assert g.can_continue and not g.earned_bonus


def test_gate_calibrated_thresholds():
    low = evaluate_gate(0.40, calibrated=True, min_advance=0.55, green=0.8, all_green=False)
    assert not low.can_continue
    mid = evaluate_gate(0.65, calibrated=True, min_advance=0.55, green=0.8, all_green=False)
    assert mid.can_continue and not mid.earned_bonus
    high = evaluate_gate(0.90, calibrated=True, min_advance=0.55, green=0.8, all_green=False)
    assert high.can_continue and high.earned_bonus


def test_gate_all_green_earns_bonus():
    g = evaluate_gate(0.70, calibrated=True, min_advance=0.55, green=0.8, all_green=True)
    assert g.earned_bonus
