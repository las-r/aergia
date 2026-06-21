import pytest
from aergia.nodes import Environment


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_chain(*binding_dicts):
    """Build a parent→child Environment chain from a list of dicts (outermost first)."""
    env = Environment(binding_dicts[0])
    for d in binding_dicts[1:]:
        child = Environment(d, parent=env)
        env = child
    return env


# ── Basic get / set / contains ────────────────────────────────────────────────

class TestBasicOperations:
    def test_set_and_get_local(self):
        env = Environment()
        env["x"] = 42
        assert env["x"] == 42

    def test_missing_key_raises(self):
        env = Environment()
        with pytest.raises(KeyError):
            _ = env["missing"]

    def test_contains_local(self):
        env = Environment({"a": 1})
        assert "a" in env
        assert "z" not in env

    def test_delete_local(self):
        env = Environment({"a": 1})
        del env["a"]
        assert "a" not in env

    def test_delete_missing_raises(self):
        env = Environment()
        with pytest.raises(KeyError):
            del env["nope"]

    def test_get_with_default(self):
        env = Environment()
        assert env.get("x", 99) == 99
        env["x"] = 5
        assert env.get("x", 99) == 5

    def test_len_flat(self):
        env = Environment({"a": 1, "b": 2, "c": 3})
        assert len(env) == 3

    def test_iter_flat(self):
        env = Environment({"a": 1, "b": 2})
        assert set(env) == {"a", "b"}


# ── Parent chain lookup ───────────────────────────────────────────────────────

class TestParentChain:
    def test_get_from_parent(self):
        parent = Environment({"x": 10})
        child = Environment(parent=parent)
        assert child["x"] == 10

    def test_contains_in_parent(self):
        parent = Environment({"x": 10})
        child = Environment(parent=parent)
        assert "x" in child

    def test_get_with_default_walks_chain(self):
        parent = Environment({"x": 10})
        child = Environment(parent=parent)
        assert child.get("x", 0) == 10
        assert child.get("y", 0) == 0

    def test_deep_chain_lookup(self):
        env = make_chain({"a": 1}, {"b": 2}, {"c": 3})
        assert env["a"] == 1
        assert env["b"] == 2
        assert env["c"] == 3

    def test_delete_in_parent(self):
        parent = Environment({"x": 10})
        child = Environment(parent=parent)
        del child["x"]
        assert "x" not in parent

    def test_iter_merges_chain(self):
        env = make_chain({"a": 1}, {"b": 2}, {"c": 3})
        assert set(env) == {"a", "b", "c"}

    def test_iter_child_shadows_parent_key(self):
        """Each key should appear only once even if present in multiple levels."""
        parent = Environment({"x": 1, "y": 2})
        child = Environment({"x": 99}, parent=parent)
        keys = list(child)
        assert keys.count("x") == 1
        assert set(keys) == {"x", "y"}

    def test_len_with_chain(self):
        parent = Environment({"a": 1, "b": 2})
        child = Environment({"c": 3}, parent=parent)
        assert len(child) == 3

    def test_len_deduplicates_shadowed_keys(self):
        parent = Environment({"x": 1, "y": 2})
        child = Environment({"x": 99}, parent=parent)
        assert len(child) == 2


# ── Assignment propagation semantics ─────────────────────────────────────────

class TestAssignmentPropagation:
    def test_new_key_goes_local(self):
        parent = Environment({"x": 1})
        child = Environment(parent=parent)
        child["new"] = 42
        assert "new" in child.bindings
        assert "new" not in parent.bindings

    def test_existing_parent_key_propagates_up(self):
        parent = Environment({"x": 1})
        child = Environment(parent=parent)
        child["x"] = 99
        assert parent["x"] == 99
        assert "x" not in child.bindings

    def test_local_key_stays_local_on_update(self):
        parent = Environment({"x": 1})
        child = Environment({"x": 10}, parent=parent)
        child["x"] = 99
        assert child.bindings["x"] == 99
        assert parent.bindings["x"] == 1

    def test_deep_propagation(self):
        """Assignment should walk all the way up to the level that owns the key."""
        grandparent = Environment({"x": 1})
        parent = Environment(parent=grandparent)
        child = Environment(parent=parent)
        child["x"] = 42
        assert grandparent.bindings["x"] == 42
        assert "x" not in parent.bindings
        assert "x" not in child.bindings

    def test_shadow_does_not_dirty_parent(self):
        """A local binding that shadows a parent key must not write through on update."""
        parent = Environment({"x": 1})
        child = Environment({"x": 10}, parent=parent)
        child["x"] = 50
        assert child.bindings["x"] == 50
        assert parent.bindings["x"] == 1


# ── copy() ────────────────────────────────────────────────────────────────────

class TestCopy:
    def test_copy_creates_child(self):
        env = Environment({"x": 1})
        child = env.copy()
        assert child.parent is env
        assert child.bindings == {}

    def test_copy_sees_parent_bindings(self):
        env = Environment({"x": 1})
        child = env.copy()
        assert child["x"] == 1

    def test_copy_new_bindings_are_local(self):
        env = Environment({"x": 1})
        child = env.copy()
        child["y"] = 2
        assert "y" not in env

    def test_copy_assignment_propagates_to_original(self):
        env = Environment({"x": 1})
        child = env.copy()
        child["x"] = 99
        assert env["x"] == 99

    def test_double_copy_propagates_through_chain(self):
        env = Environment({"x": 1})
        mid = env.copy()
        leaf = mid.copy()
        leaf["x"] = 42
        assert env["x"] == 42

    def test_local_bindings_do_not_bleed_into_parent_after_copy(self):
        env = Environment({"x": 1})
        child = env.copy()
        child["shadow"] = 999
        assert "shadow" not in env

    def test_copy_chain_depth(self):
        env = Environment({"a": 1})
        c1 = env.copy()
        c2 = c1.copy()
        c3 = c2.copy()
        assert c3["a"] == 1
        assert c3.parent is c2
        assert c2.parent is c1
        assert c1.parent is env
