from app.utils import group_emails_by_domain

def test_grouping_basic():
    emails = ["a@x.com", "b@y.com", "c@x.com"]
    grouped = group_emails_by_domain(emails)
    assert grouped["x.com"] == ["a@x.com", "c@x.com"]
    assert grouped["y.com"] == ["b@y.com"]
