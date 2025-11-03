# small helpers if needed later
def group_emails_by_domain(email_list):
    from collections import defaultdict
    grouped = defaultdict(list)
    for e in email_list:
        if "@" in e:
            domain = e.split("@", 1)[1].lower()
            grouped[domain].append(e)
    return grouped
