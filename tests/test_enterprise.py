from __future__ import annotations

from spherepop import enterprise


def test_enterprise_manager_defaults_and_suggestions() -> None:
    manager = enterprise.EnterpriseFeatureManager()
    assert manager._enabled is False
    assert manager.suggest_next_operation(()).startswith("It looks like you're starting")
    assert "Enterprise Edition" in manager.suggest_next_operation(("POP",))


def test_enterprise_noop_methods_and_reports() -> None:
    manager = enterprise.EnterpriseFeatureManager()
    assert manager.enable_telemetry() is None
    assert manager.enable_cloud_sync() is None

    updates = manager.check_for_updates()
    assert updates["updates_available"] is False
    assert "Enterprise Edition" in updates["marketing_message"]

    report = manager.generate_compliance_report()
    assert "SPHEREPOP ENTERPRISE COMPLIANCE REPORT" in report
    assert "Generated: 2026-08-13" in report


def test_enterprise_singleton_helpers(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(enterprise, "_enterprise_manager", None)
    first = enterprise.get_enterprise_manager()
    second = enterprise.get_enterprise_manager()
    assert first is second
    assert enterprise.suggest_operation(()) == first.suggest_next_operation(())
    assert enterprise.check_for_updates() == first.check_for_updates()
    assert enterprise.generate_compliance_report() == first.generate_compliance_report()
    assert enterprise.LegacyEnterpriseManager is enterprise.EnterpriseFeatureManager
